'''
Main goal is to match up VIIRS data and landsat data.

Here we use doy of landsat as the doy of data sample
'''

import h5py
import os
import logging
import numpy as np

logging.basicConfig(filename="ML.Data.log", level=logging.INFO,
                    format='%(asctime)s %(message)s',
                    filemode='w')

viirspath = '/net/airs1/storage/people/mgcy/Projects/VIIRS_Super_Resolution/VIIRS_VI_HW/'
landsatpath = '/net/airs1/storage/people/mgcy/Projects/VIIRS_Super_Resolution/Landsat_VI_MVC_HW/'
savepath = '/net/airs1/storage/people/mgcy/Projects/VIIRS_Super_Resolution/ML_VI_MVC_Data_HW/'

workpath = '/net/airs1/storage/people/mgcy/Projects/VIIRS_Super_Resolution/'

x_mask = np.load(workpath + 'Masks/Mask.480m.npy')
y_mask = np.load(workpath + 'Masks/Mask.30m.npy')


viirs_start_doy_dict = {'2018':'9',
                  '2019':'17',
                  '2020':'1',
                  '2021':'1',
                  '2022':'9',
                  '2023':'9',}

landsat_start_doy_dict = {'2018':'13',
                  '2019':'16',
                  '2020':'3',
                  '2021':'5',
                  '2022':'8',
                  '2023':'11',}

def make_ML_data(start_year, end_year, type='Train'):
    for year in range(start_year, end_year):
        year = str(year)
        viirs_start_doy = int(viirs_start_doy_dict[year])
        landsat_start_doy = int(landsat_start_doy_dict[year])
        
        while int(viirs_start_doy) <= 365:
            landsat_start_doy = str(landsat_start_doy).zfill(3)
            logging.info('Landsat doy: ' + year + ' ' +  landsat_start_doy)
            viirs_start_doy = str(viirs_start_doy).zfill(3)
            logging.info('VIIRS doy: ' + year + ' ' +  viirs_start_doy)
            
            VIIRS_FLAG = True
            LANDSAT_FLAG = True
            # load VIIRS
            try:
                viirs_tmp = np.load(viirspath + 'VIIRS.VNP13.VI.' + year + '.' + str(viirs_start_doy) + '.npy') / 10000.0
            except:
                logging.info('VIIRS Missing @ ' + year + '-' + viirs_start_doy)
                VIIRS_FLAG = False
            
            # load Landsat
            try:
                landsat_tmp = np.load(landsatpath + 'Landsat.VI.MVC.' + year + '.' + str(landsat_start_doy) + '.npy')
            except:
                logging.info('Landsat Missing @ ' + year + '-' + landsat_start_doy)
                LANDSAT_FLAG = False
            
            # make data if both exist
            if VIIRS_FLAG and LANDSAT_FLAG:
                viirs_tmp[viirs_tmp==-1.5] = 0
                viirs_tmp[viirs_tmp>=1] = 1
                viirs_tmp[viirs_tmp<=-1] = -1
                
                landsat_tmp[landsat_tmp>=1] = 1
                landsat_tmp[landsat_tmp<=-1] = -1

                landsat_tmp = np.where(np.isnan(landsat_tmp), 0, landsat_tmp)

                # apply masks
                viirs_tmp[0] = viirs_tmp[0] * x_mask
                viirs_tmp[1] = viirs_tmp[1] * x_mask
                viirs_tmp[2] = viirs_tmp[2] * x_mask

                landsat_tmp[0] = landsat_tmp[0] * y_mask
                landsat_tmp[1] = landsat_tmp[1] * y_mask
                landsat_tmp[2] = landsat_tmp[2] * y_mask
                
                logging.info('Make ML Data : ' +  year + ' - ' +  landsat_start_doy)
                file = h5py.File(savepath + type + '/VI.' + year + '.' + str(landsat_start_doy) + '.HW.h5', 'w')
                file.create_dataset('viirs', data = viirs_tmp)
                file.create_dataset('landsat', data = landsat_tmp)
                file.close()

            landsat_start_doy = int(landsat_start_doy) + 16
            viirs_start_doy = int(viirs_start_doy) + 16

# make_ML_data(2018, 2021, type='Train')
make_ML_data(2019, 2024, type='Test')
