# This program is to train a VegGAN for downscaling VIIRS VI data 
# to 30 meters resolution.
# Copyright @ 2021-2026 | Colorado State University, Fort Collins, CO, USA
# Yifan Yang and Haonan Chen (haonan.chen@colostate.edu)
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# -----------------------------------------------------

import torch.nn as nn
import torch
from torchvision.models import vgg19
import matplotlib.pyplot as plt

def plot_example(viirs, landsat, sr_viirs, interpolation, batches_done):
    '''
    Plot the example images for the training process
    :param viirs: VIIRS image
    :param landsat: Landsat image
    :param sr_viirs: Super-resolved VIIRS image
    :param interpolation: Interpolated image
    :param batches_done: Current batch number
    :return: None
    '''
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))

    im1 = axes[0,0].imshow(viirs, cmap='RdYlGn', vmin=-1.5, vmax=1.5)
    axes[0,0].set_title('VIIRS')
    plt.colorbar(im1, fraction=0.04, pad=0.025)

    im2 = axes[0, 1].imshow(landsat, cmap='RdYlGn', vmin=-1.5, vmax=1.5)
    axes[0, 1].set_title('Landsat')
    plt.colorbar(im2, fraction=0.04, pad=0.025)

    im3 = axes[1, 0].imshow(sr_viirs, cmap='RdYlGn', vmin=-1.5, vmax=1.5)
    axes[1, 0].set_title('SR-VIIRS')
    plt.colorbar(im3, fraction=0.04, pad=0.025)

    im4 = axes[1, 1].imshow(interpolation, cmap='RdYlGn', vmin=-1.5, vmax=1.5)
    axes[1, 1].set_title('Interpolation')
    plt.colorbar(im4, fraction=0.04, pad=0.025)

    # save figure
    plt.savefig("/nfs/home/yyang/Projects/VIIRS_SR16/Code/train_img/Train.%d.png" % batches_done, format='png',
                bbox_inches='tight') #facecolor=(1, 1, 1, 0)
    plt.close();
    

class FeatureExtractor(nn.Module):
    '''
    Feature extractor using VGG19 model
    :param: None
    :return: None
    '''
    def __init__(self):
        super(FeatureExtractor, self).__init__()
        vgg19_model = vgg19(pretrained=True)
        self.vgg19_54 = nn.Sequential(*list(vgg19_model.features.children())[:35])
        # first_conv_layer = [nn.Conv2d(1, 3, kernel_size=3, stride=1, padding=1, dilation=1, groups=1, bias=True)]
        # first_conv_layer.extend(list(vgg19_model.features.children())[:35])
        # self.feature_extractor = nn.Sequential(*first_conv_layer)

    def forward(self, img):
        return self.vgg19_54(img)
        # return self.feature_extractor(img)



class DenseResidualBlock(nn.Module):
    """
    The core module of paper: (Residual Dense Network for Image Super-Resolution, CVPR 18)
    """

    def __init__(self, filters, res_scale=0.2):
        super(DenseResidualBlock, self).__init__()
        self.res_scale = res_scale

        def block(in_features, non_linearity=True):
            '''
            Dense block
            :param in_features: input features
            :param non_linearity: if True, add non-linearity
            :return: layers
            '''
            layers = [nn.Conv2d(in_features, filters, 3, 1, 1, bias=True)]
            if non_linearity:
                layers += [nn.LeakyReLU()]
            return nn.Sequential(*layers)

        self.b1 = block(in_features=1 * filters)
        self.b2 = block(in_features=2 * filters)
        self.b3 = block(in_features=3 * filters)
        self.b4 = block(in_features=4 * filters)
        self.b5 = block(in_features=5 * filters, non_linearity=False)
        self.blocks = [self.b1, self.b2, self.b3, self.b4, self.b5]

    def forward(self, x):
        inputs = x
        for block in self.blocks:
            out = block(inputs)
            inputs = torch.cat([inputs, out], 1)
        return out.mul(self.res_scale) + x


class ResidualInResidualDenseBlock(nn.Module):
    '''
    Residual in Residual Dense Block
    The core module of paper: (Enhanced Deep Residual Networks for Single Image Super-Resolution, CVPR 2017)
    '''
    def __init__(self, filters, res_scale=0.2):
        super(ResidualInResidualDenseBlock, self).__init__()
        self.res_scale = res_scale
        self.dense_blocks = nn.Sequential(
            DenseResidualBlock(filters), DenseResidualBlock(filters), DenseResidualBlock(filters)
        )

    def forward(self, x):
        return self.dense_blocks(x).mul(self.res_scale) + x


class GeneratorRRDB(nn.Module):
    '''
    Generator using RRDB blocks
    The core module of paper: (ESRGAN: Enhanced Super-Resolution Generative Adversarial Networks, ECCV 2018)
    '''
    def __init__(self, channels=3, filters=64, num_res_blocks=16, num_upsample=2):
        super(GeneratorRRDB, self).__init__()

        # First layer
        self.conv1 = nn.Conv2d(channels, filters, kernel_size=3, stride=1, padding=1)
        # Residual blocks
        self.res_blocks = nn.Sequential(*[ResidualInResidualDenseBlock(filters) for _ in range(num_res_blocks)])
        # Second conv layer post residual blocks
        self.conv2 = nn.Conv2d(filters, filters, kernel_size=3, stride=1, padding=1)
        # Upsampling layers
        upsample_layers = []
        for _ in range(num_upsample):
            upsample_layers += [
                nn.Conv2d(filters, filters * 4, kernel_size=3, stride=1, padding=1),
                nn.LeakyReLU(),
                nn.PixelShuffle(upscale_factor=2),
            ]
        self.upsampling = nn.Sequential(*upsample_layers)
        # Final output block
        self.conv3 = nn.Sequential(
            nn.Conv2d(filters, filters, kernel_size=3, stride=1, padding=1),
            nn.LeakyReLU(),
            nn.Conv2d(filters, channels, kernel_size=3, stride=1, padding=1),
        )

    def forward(self, x):
        out1 = self.conv1(x)
        out = self.res_blocks(out1)
        out2 = self.conv2(out)
        out = torch.add(out1, out2)
        out = self.upsampling(out)
        out = self.upsampling(out)
        out = self.conv3(out)
        return out


class Discriminator(nn.Module):
    '''
    Discriminator using PatchGAN
    The core module of paper: (Image-to-Image Translation with Conditional Adversarial Networks, CVPR 2017)
    '''
    def __init__(self, input_shape):
        super(Discriminator, self).__init__()

        self.input_shape = input_shape
        in_channels, in_height, in_width = self.input_shape
        patch_h, patch_w = int(in_height / 2 ** 4), int(in_width / 2 ** 4)
        self.output_shape = (1, patch_h, patch_w)

        def discriminator_block(in_filters, out_filters, first_block=False):
            '''
            Discriminator block
            :param in_filters: input filters
            :param out_filters: output filters
            :param first_block: if first block, no batch norm
            :return: layers
            '''
            layers = []
            layers.append(nn.Conv2d(in_filters, out_filters, kernel_size=3, stride=1, padding=1))
            if not first_block:
                layers.append(nn.BatchNorm2d(out_filters))
            layers.append(nn.LeakyReLU(0.2, inplace=True))
            layers.append(nn.Conv2d(out_filters, out_filters, kernel_size=3, stride=2, padding=1))
            layers.append(nn.BatchNorm2d(out_filters))
            layers.append(nn.LeakyReLU(0.2, inplace=True))
            return layers

        layers = []
        in_filters = in_channels
        for i, out_filters in enumerate([64, 128, 256, 512]):
            layers.extend(discriminator_block(in_filters, out_filters, first_block=(i == 0)))
            in_filters = out_filters

        layers.append(nn.Conv2d(out_filters, 1, kernel_size=3, stride=1, padding=1))

        self.model = nn.Sequential(*layers)

    def forward(self, img):
        return self.model(img)