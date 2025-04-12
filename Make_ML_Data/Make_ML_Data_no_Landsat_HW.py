'''
Main goal is to match up VIIRS data and landsat data.

Here we use doy of landsat as the doy of data sample
'''

import h5py
import logging
import numpy as np

logging.basicConfig(filename="ML.Data.log", level=logging.INFO,
                    format='%(asctime)s %(message)s',
                    filemode='w')

viirspath = '/net/airs1/storage/people/mgcy/Projects/VIIRS_Super_Resolution/VIIRS_VI_Test_All_Islands/'
savepath = '/net/airs1/storage/people/mgcy/Projects/VIIRS_Super_Resolution/ML_VI_Data_noLandsat_HW/'

viirs_start_doy_dict = {'2018':'9',
                  '2019':'17',
                  '2020':'1',
                  '2021':'1',
                  '2022':'9',
                  '2023':'9',}

def make_ML_data(start_year, end_year, type='Train'):
    for year in range(start_year, end_year):
        year = str(year)
        viirs_start_doy = int(viirs_start_doy_dict[year]) + 8
        
        while int(viirs_start_doy) <= 365:
            viirs_start_doy = str(viirs_start_doy).zfill(3)
            logging.info('VIIRS doy: ' + year + ' ' +  viirs_start_doy)
            
            VIIRS_FLAG = True
            # load VIIRS
            try:
                viirs_tmp = np.load(viirspath + 'VIIRS.VNP13.VI.' + year + '.' + str(viirs_start_doy) + '.npy')
            except:
                logging.info('VIIRS Missing @ ' + year + '-' + viirs_start_doy)
                VIIRS_FLAG = False
            
            
            # make data if exists
            if VIIRS_FLAG:
                logging.info('Make ML Data : ' +  year + ' - ' +  viirs_start_doy)
                file = h5py.File(savepath + type + '.VI.' + year + '.' + str(viirs_start_doy) + '_no_Landsat.HW.h5', 'w')
                file.create_dataset('viirs', data = viirs_tmp)
                file.close()

            viirs_start_doy = int(viirs_start_doy) + 16

# make_ML_data(2018, 2021, type='Train_no_Landsat')
make_ML_data(2018, 2024, type='Test_no_Landsat')
