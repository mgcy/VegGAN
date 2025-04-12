# This program is to test the trained VegGAN for downscaling VIIRS VI data 
# to 30 meters resolution.
# Copyright @ 2021-2026 | Colorado State University, Fort Collins, CO, USA
# Yifan Yang and Haonan Chen (haonan.chen@colostate.edu)
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# -----------------------------------------------------


import torch
from torch.autograd import Variable
import torch.nn as nn
import os
import numpy as np
import h5py

workpath = '/nfs/home/yyang/Projects/VIIRS_SR16/'

from models import GeneratorRRDB

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(device)

Tensor = torch.cuda.FloatTensor if torch.cuda.is_available() else torch.Tensor

class HpyerParameters:
    '''
    Hyper-Parameters
    '''
    def __init__(self):
        self.checkpoint_model = workpath + 'Code/saved_models/generator.pth'
                                        # path to checkpoint model
        self.channels = 3               # number of image channels
        self.residual_blocks = 16       # number of residual blocks in G

opt = HpyerParameters()

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Define model and load model checkpoint
generator = GeneratorRRDB(opt.channels, filters=64, num_res_blocks=opt.residual_blocks).to(device)
generator.load_state_dict(torch.load(opt.checkpoint_model))
generator.eval()


# load  folder
filelist = os.listdir(workpath + 'Data/SR_VI_MVC_Data_HW/Test/')
filelist.sort()
len_file = len(filelist)

for i in range(len_file):
#for i in range(10):
    file = h5py.File(workpath + 'Data/SR_VI_MVC_Data_HW/Test/' + filelist[i], 'r')
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

    # convert to pytorch tensor
    imgs_lr = Variable(tmp_lr.type(Tensor))
    imgs_hr = Variable(tmp_hr.type(Tensor))

    gen_hr = generator(imgs_lr)

    intero = nn.functional.interpolate(imgs_lr, scale_factor=16, mode='bicubic')

    np.save(workpath + 'Variables/Test_Interpolation_HW/' + filelist[i][:-3] + '.npy', intero[0].cpu())
    np.save(workpath + 'Variables/Test_SR_HW/' + filelist[i][:-3] + '.npy', gen_hr[0].cpu().detach().numpy())
