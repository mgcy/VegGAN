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

from torch.autograd import Variable
import torch.nn as nn
import torch
import numpy as np

workpath = '/nfs/home/yyang/Projects/VIIRS_SR16/'

from models import GeneratorRRDB, Discriminator, plot_example, FeatureExtractor

import datetime as dt
import os
from random import shuffle
import h5py

# monitor start time
start_time = dt.datetime.now()
print('Start learning at {}'.format(str(start_time)))

# ------------------
#  Hyper-Parameters
# ------------------

class HpyerParameters:
    ''' Hyper-parameters for the model training '''
    def __init__(self):
        self.load_model = 0             # load previously trained model
        self. n_epochs = 400            # number of epochs of Training
        self.lr = 0.00005               # adam: learning rate
        self.b1 = 0.9                   # adam: decay of first order momentum of gradien
        self.b2 = 0.999                 # adam: decay of second order momentum of gradien
        self.n_cpu = 0                  # number of cpu threads to use during batch generation
        self.hr_height = 2656           # high res. image height
        self.hr_width = 2656            # high res. image width
        self.channels = 3               # number of image channels
        self.sample_interval = 5        # interval between saving image samples
        self.checkpoint_interval = 5    # epoch interval between model checkpoints
        self.residual_blocks = 8        # number of residual blocks in the generator
        self.lambda_adv = 0.02          # adversarial loss weight
        self.lambda_pixel = 20          # pixel-wise loss weight

opt = HpyerParameters()

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

hr_shape = (opt.hr_height, opt.hr_width)

# Initialize generator and discriminator
generator = GeneratorRRDB(opt.channels, filters=64, num_res_blocks=opt.residual_blocks).to(device)
discriminator = Discriminator(input_shape=(opt.channels, *hr_shape)).to(device)
feature_extractor = FeatureExtractor().to(device)

# Set feature extractor to inference mode
feature_extractor.eval()

# Losses
criterion_GAN = torch.nn.BCEWithLogitsLoss().to(device)
criterion_content = torch.nn.MSELoss().to(device)
criterion_pixel = torch.nn.MSELoss().to(device)

if opt.load_model:
    # Load pretrained models
    generator.load_state_dict(torch.load(workpath + "Code/saved_models/generator.pth"))
    discriminator.load_state_dict(torch.load(workpath + "Code/saved_models/discriminator.pth"))

# Optimizers
optimizer_G = torch.optim.Adam(generator.parameters(), lr=opt.lr, betas=(opt.b1, opt.b2))
optimizer_D = torch.optim.Adam(discriminator.parameters(), lr=opt.lr, betas=(opt.b1, opt.b2))

Tensor = torch.cuda.FloatTensor if torch.cuda.is_available() else torch.Tensor

# ----------
#  Training
# ----------
# load training folder
train_filelist = os.listdir(workpath + 'Data/SR_VI_Data_HW/Train/')
train_filelist.sort()
len_train = len(train_filelist)

for epoch in range(0, opt.n_epochs):
    # shuffle
    shuffle(train_filelist)

    for i in range(len_train):
        batches_done = epoch * len_train + i

        # Configure model input
        file = h5py.File(workpath + 'Data/SR_VI_Data_HW/Test/' + train_filelist[i], 'r')
        tmp_lr = np.array(file['viirs'][:])
        tmp_hr = np.array(file['landsat'][:])
        file.close()

        # initilize
        pad_lr = np.zeros((3, 166, 166))
        pad_hr = np.zeros((3, 2656, 2656))

        pad_lr[:, :125, :166] = tmp_lr
        pad_hr[:, :2000, :2656] = tmp_hr

        tmp_lr = Tensor(pad_lr)
        tmp_hr = Tensor(pad_hr)

        tmp_lr = torch.reshape(tmp_lr, (1, 3, 166, 166))
        tmp_hr = torch.reshape(tmp_hr, (1, 3, 2656, 2656))

        # covert to pytorch tensor
        imgs_lr = Variable(tmp_lr.type(Tensor))
        imgs_hr = Variable(tmp_hr.type(Tensor))

        # Adversarial ground truths
        valid = Variable(Tensor(np.ones((imgs_lr.size(0), *discriminator.output_shape))), requires_grad=False)
        fake = Variable(Tensor(np.zeros((imgs_lr.size(0), *discriminator.output_shape))), requires_grad=False)

        # ------------------
        #  Train Generators
        # ------------------

        optimizer_G.zero_grad()

        # Generate a high resolution image from low resolution input
        gen_hr = generator(imgs_lr)

        # Measure pixel-wise loss against ground truth
        loss_pixel = criterion_pixel(gen_hr, imgs_hr)

        # Extract validity predictions from discriminator
        pred_real = discriminator(imgs_hr).detach()
        pred_fake = discriminator(gen_hr)

        # Adversarial loss (relativistic average GAN)
        loss_GAN = criterion_GAN(pred_fake - pred_real.mean(0, keepdim=True), valid)

        # Content loss
        gen_features = feature_extractor(gen_hr[:,:3])
        real_features = feature_extractor(imgs_hr[:,:3]).detach()
        loss_content = criterion_content(gen_features, real_features)

        # Total generator loss
        loss_G = loss_content + opt.lambda_adv * 0.5 * loss_GAN + opt.lambda_pixel * loss_pixel

        loss_G.backward()
        optimizer_G.step()

        # ---------------------
        #  Train Discriminator
        # ---------------------

        # print('Train Discriminator')
        optimizer_D.zero_grad()

        pred_real = discriminator(imgs_hr)
        pred_fake = discriminator(gen_hr.detach())

        # Adversarial loss for real and fake images (relativistic average GAN)

        loss_real = criterion_GAN(pred_real - pred_fake.mean(0, keepdim=True), valid)
        loss_fake = criterion_GAN(pred_fake - pred_real.mean(0, keepdim=True), fake)

        # Total loss
        loss_D = (loss_real + loss_fake) / 0.001

        loss_D.backward()
        optimizer_D.step()

    # -----------------------
    #  Log Progress per Epoch
    # -----------------------

    print(
        "[Epoch %d/%d] [D loss: %f] [G loss: %f, content: %f, adv: %f, pixel: %f]"
        % (
            epoch,
            opt.n_epochs,
            loss_D.item(),
            loss_G.item(),
            loss_content.item(),
            loss_GAN.item(),
            loss_pixel.item(),
        )
    )

    if epoch % opt.sample_interval == 0:
        # Save image grid with upsampled inputs and ESRGAN outputs
        intero = nn.functional.interpolate(imgs_lr, scale_factor=16, mode='bicubic')
        # print(gen_hr.shape)
        plot_example(imgs_lr[0, 0].cpu(), imgs_hr[0, 0].cpu(), gen_hr[0, 0].cpu().detach().numpy(), intero[0, 0].cpu(), epoch)

    if epoch % opt.checkpoint_interval == 0:
        # Save model checkpoints
        torch.save(generator.state_dict(), workpath + "Code/saved_models/generator.pth")
        torch.save(discriminator.state_dict(), workpath + "Code/saved_models/discriminator.pth")

# monitor end time
end_time = dt.datetime.now()
print('Stop learning {}'.format(str(end_time)))
elapsed_time = end_time - start_time
print('Elapsed learning {}'.format(str(elapsed_time)))
