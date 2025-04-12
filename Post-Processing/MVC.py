'''
This code is used to generate composite Landsat VI product 
using Max Value Composition (MVC).

Method: for doy i, VI_i = max(VI_{i-16}, VI_{i}, VI_{i+16})

'''

import logging
import numpy as np
import os

logging.basicConfig(filename="MVC.Landsat.log", level=logging.INFO,
                    format='%(asctime)s %(message)s',
                    filemode='w')

workpath = '/net/airs1/storage/people/mgcy/Projects/VIIRS_Super_Resolution/'

landsatpath = workpath + '16/VI_Test_All_Islands_for_EVI/'
savepath = workpath + '16/VI_Test_All_Islands_for_EVI_MVC/'

os.makedirs(savepath, exist_ok=True)

landsat_start_doy_dict = {
                  '2014':'10',
                  '2015':'13',
                  '2016':'16',
                  '2017':'2',
                  '2018':'5',
                  '2019':'8',
                  '2020':'11',
                  '2021':'13',
                  '2022':'16',
                  '2023':'201',}

def MVC():
    for year in range(2023, 2024):
        year = str(year)
        landsat_start_doy = int(landsat_start_doy_dict[year])
        
        while int(landsat_start_doy) <= 365:
            before_doy = int(landsat_start_doy) - 8
            after_doy = int(landsat_start_doy) + 8
            
            before_doy2 = int(landsat_start_doy) - 16
            after_doy2 = int(landsat_start_doy) + 16
            
            
            # fill to 3 digits
            landsat_start_doy = str(landsat_start_doy).zfill(3)
            before_doy = str(before_doy).zfill(3)
            after_doy = str(after_doy).zfill(3)
            before_doy2 = str(before_doy2).zfill(3)
            after_doy2 = str(before_doy2).zfill(3)
            
            BEFORE_FLAG = True
            AFTER_FLAG = True
            BEFORE2_FLAG = True
            AFTER2_FLAG = True
            
            # load Landsat this day
            try:
                landsat_itself = np.load(landsatpath + 'SR.VNP13.VI.Test.' + year + '.' + str(landsat_start_doy) + '.npy')
            except:
                logging.info('Itself Missing @ ' + year + '-' + landsat_start_doy)
                continue
            
            # load Landsat before
            try:
                landsat_before = np.load(landsatpath + 'SR.VNP13.VI.Test.' + year + '.' + str(before_doy) + '.npy')
            except:
                logging.info('Before Missing @ ' + year + '-' + landsat_start_doy)
                BEFORE_FLAG = False
            
            # load Landsat before
            try:
                landsat_after = np.load(landsatpath + 'SR.VNP13.VI.Test.' + year + '.' + str(after_doy) + '.npy')
            except:
                logging.info('After Missing @ ' + year + '-' + landsat_start_doy)
                AFTER_FLAG = False
                
            # load Landsat before
            try:
                landsat2_before = np.load(landsatpath + 'SR.VNP13.VI.Test.' + year + '.' + str(before_doy2) + '.npy')
            except:
                logging.info('Before2 Missing @ ' + year + '-' + landsat_start_doy)
                BEFORE2_FLAG = False
            
            # load Landsat before
            try:
                landsat2_after = np.load(landsatpath + 'SR.VNP13.VI.Test.' + year + '.' + str(after_doy2) + '.npy')
            except:
                logging.info('After2 Missing @ ' + year + '-' + landsat_start_doy)
                AFTER2_FLAG = False
                        
            # make data if exists
            if BEFORE_FLAG:
                landsat_itself = np.maximum(landsat_before, landsat_itself)
                 
            if BEFORE2_FLAG:
                landsat_itself = np.maximum(landsat2_before, landsat_itself)
            
            if AFTER_FLAG:
                landsat_itself = np.maximum(landsat_after, landsat_itself)
            
            if AFTER2_FLAG:
                landsat_itself = np.maximum(landsat2_after, landsat_itself)    
            
            np.save(savepath + 'SR.VNP13.VI.Test.' + year + '.' + str(landsat_start_doy) + '.npy', landsat_itself)
            landsat_start_doy = int(landsat_start_doy) + 8

MVC()