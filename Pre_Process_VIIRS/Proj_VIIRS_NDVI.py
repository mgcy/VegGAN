import cartopy
import numpy as np
import os
import netCDF4 as nc
from cartopy import crs as ccrs
import cartopy.img_transform as im_trans
import logging

logging.basicConfig(filename="Proj.VIIRS.log", level=logging.INFO,
                    format='%(asctime)s %(message)s',
                    filemode='w')

savepath = '/net/airs1/storage/people/mgcy/Projects/VIIRS_Super_Resolution/VIIRS_NDVI/'

start_doy_dict = {'2015':'10', 
                  '2016':'13',
                  '2017':'15',
                  '2018':'2',
                  '2019':'5',
                  '2020':'8',
                  '2021':'10',
                  '2022':'13',}


for year in range(2017,2023):
    year = str(year)
    start_doy = start_doy_dict[year]
    for doy in range(int(start_doy), 366, 16):
        doy = str(doy).zfill(3)
        logging.info(year + ' ' +  doy)
        # load VNP02
        errorflag02 = True
        vnp02path = '/net/airs1/storage/people/mgcy/Data/VIIRS_CO_raw/VNP02IMG/' + \
            year + '/' + str(doy)
        try:
            vnp02file = os.listdir(vnp02path)
        except:
            logging.info('VNP02 Missing @ ' + doy)
            continue
        # if file exists
        if len(vnp02file) != 1:
            logging.info('VNP02 not one file @ ' + doy)
            continue
        elif str(doy) not in vnp02file[0]:
            logging.info('VNP02 DOY mis-mismatch @ ' + doy)
            continue
        else:
            NC = nc.Dataset(vnp02path + '/' + vnp02file[0])
            obv_data = NC.groups['observation_data']
            nir_data_sr = np.array(obv_data.variables['I02'][:])
            red_data_sr = np.array(obv_data.variables['I01'][:])

            errorflag02 = False

        # load VNP03
        errorflag03 = True
        vnp03path = '/net/airs1/storage/people/mgcy/Data/VIIRS_CO_raw/VNP03IMG/' + \
            year + '/' + str(doy)
            
        try:
            vnp03file = os.listdir(vnp03path)
        except:
            logging.info('VNP02 Missing @ ' + doy)
            continue
        # if file exists
        if len(vnp03file) != 1:
            logging.info('VNP03 not one file @ ' + doy)
            continue
        elif str(doy) not in vnp03file[0]:
            logging.info('VNP03 DOY mis-mismatch @ ' + doy)
            continue
        else:
            NC = nc.Dataset(vnp03path + '/' + vnp03file[0])
            geo_data = NC.groups['geolocation_data']
            lat = np.array(geo_data.variables['latitude'][:])
            lon = np.array(geo_data.variables['longitude'][:])

            errorflag03 = False

        if errorflag02 == False and errorflag03 == False:
            source_cs = ccrs.Geodetic()

            SouthBoundingCoordinate = 40.0
            NorthBoundingCoordinate = 41.0
            WestBoundingCoordinate = -106.0
            EastBoundingCoordinate = -105.0

            # Target grid
            target_nx = int(
                (EastBoundingCoordinate - WestBoundingCoordinate) / 0.00375)
            target_ny = int((NorthBoundingCoordinate -
                            SouthBoundingCoordinate) / 0.00375)
            target_proj = ccrs.PlateCarree()

            target_lon = np.linspace(
                WestBoundingCoordinate, EastBoundingCoordinate, target_nx)
            target_lat = np.linspace(
                NorthBoundingCoordinate, SouthBoundingCoordinate, target_ny)
            target_lon2d, target_lat2d = np.meshgrid(target_lon, target_lat)

            # Perform regrid
            logging.info('regrid @ '+ doy)
            nir_data_proj = im_trans.regrid(nir_data_sr, lon, lat, source_cs,
                                            target_proj, target_lon2d, target_lat2d)
            red_data_proj = im_trans.regrid(red_data_sr, lon, lat, source_cs,
                                            target_proj, target_lon2d, target_lat2d)

            ndvi = (nir_data_proj - red_data_proj) / \
                (nir_data_proj + red_data_proj)

            np.save(savepath + 'VIIRS.NDVI.' + year + '.' + str(doy) + '.npy', ndvi)
        else:
            logging.info('Data issue : ' +  errorflag02 + '-'+ errorflag03 + ' @ ' +  doy)
