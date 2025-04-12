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

landsatpath = '/net/airs1/storage/people/mgcy/Projects/VIIRS_Super_Resolution/Landsat_VI_HW/'
savepath = '/net/airs1/storage/people/mgcy/Projects/VIIRS_Super_Resolution/Landsat_VI_MVC_HW/'

os.makedirs(savepath, exist_ok=True)

landsat_start_doy_dict = {'2018':'13',
                  '2019':'16',
                  '2020':'3',
                  '2021':'5',
                  '2022':'8',
                  '2023':'11',}

def MVC():
    for year in range(2018, 2024):
        year = str(year)
        landsat_start_doy = int(landsat_start_doy_dict[year])
        
        while int(landsat_start_doy) <= 365:
            before_doy = int(landsat_start_doy) - 16
            after_doy = int(landsat_start_doy) + 16
            
            # fill to 3 digits
            landsat_start_doy = str(landsat_start_doy).zfill(3)
            before_doy = str(before_doy).zfill(3)
            after_doy = str(after_doy).zfill(3)
            
            ITSELF_FLAG = True
            BEFORE_FLAG = True
            AFTER_FLAG = True
            
            
            # load Landsat this day
            try:
                landsat_itself = np.load(landsatpath + 'Landsat.VI.' + year + '.' + str(landsat_start_doy) + '.npy')
            except:
                logging.info('Itself Missing @ ' + year + '-' + landsat_start_doy)
                ITSELF_FLAG = False
            
            # load Landsat before
            try:
                landsat_before = np.load(landsatpath + 'Landsat.VI.' + year + '.' + str(before_doy) + '.npy')
            except:
                logging.info('Before Missing @ ' + year + '-' + landsat_start_doy)
                BEFORE_FLAG = False
            
            # load Landsat before
            try:
                landsat_after = np.load(landsatpath + 'Landsat.VI.' + year + '.' + str(after_doy) + '.npy')
            except:
                logging.info('After Missing @ ' + year + '-' + landsat_start_doy)
                AFTER_FLAG = False
                        
            # make data if both exist
            if BEFORE_FLAG and AFTER_FLAG and ITSELF_FLAG:
                logging.info('Making Data @ ' + year + '-' + landsat_start_doy)
                np.save(savepath + 'Landsat.VI.MVC.' + year + '.' + str(landsat_start_doy) + '.npy', np.maximum(landsat_before, landsat_itself,  landsat_after))
            elif ITSELF_FLAG:
                np.save(savepath + 'Landsat.VI.MVC.' + year + '.' + str(landsat_start_doy) + '.npy', landsat_itself)
            landsat_start_doy = int(landsat_start_doy) + 16

MVC()