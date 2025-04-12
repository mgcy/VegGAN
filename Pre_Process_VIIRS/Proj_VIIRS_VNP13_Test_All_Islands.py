import cartopy
import numpy as np
import os
import matplotlib.pyplot as plt
from cartopy import crs as ccrs
import cartopy.img_transform as im_trans
import logging
import h5py
import re
import pyproj
import warnings
warnings.filterwarnings('ignore')

logging.basicConfig(filename="Proj.VIIRS.allIsland.log", level=logging.INFO,
                    format='%(asctime)s %(message)s',
                    filemode='w')

savepath = '/net/airs1/storage/people/mgcy/Projects/VIIRS_Super_Resolution/VIIRS_VI_Test_All_Islands_for_EVI/'

start_doy_dict = {'2018': '9',
                  '2019': '1',
                  '2020': '1',
                  '2021': '1',
                  '2022': '1',
                  '2023': '1', }

Island_list = ['Maui', 'Oahu', 'Molokai', 'Kauai', 'Niihau',
               'Hawaii_ul', 'Hawaii_ur', 'Hawaii_ml', 'Hawaii_mr', 'Hawaii_bl', 'Hawaii_br']
Island_abox = {'Maui': [-156.75, 20.45, -155.95, 21.05],
               'Oahu': [-158.4, 21.2, -157.6, 21.8],
               'Molokai': [-157.35, 20.7, -157.35 + 0.8, 20.7 + 0.6],
               'Kauai': [-159.9, 21.8, -159.1, 22.4],
               'Niihau': [-160.7, 21.6, -160.7 + 0.8, 21.6 + 0.6],
               'Hawaii_ul': [-155.4 - 0.8, 19.7, - 155.4, 19.7 + 0.6],
               'Hawaii_ur': [-155.6, 19.7, -155.6 + 0.8, 19.7 + 0.6],
               'Hawaii_ml': [-155.4 - 0.8, 19.3, -155.4, 19.3 + 0.6],
               'Hawaii_mr': [-155.6, 19.3, -155.6 + 0.8, 19.3 + 0.6],
               'Hawaii_bl': [-155.4 - 0.8, 18.9, -155.4, 18.9 + 0.6],
               'Hawaii_br': [-155.6, 18.9, -155.6 + 0.8, 18.9 + 0.6]}


def get_rad_lat_lon(vnp13path, vnp13file):

    f = h5py.File(vnp13path + '/' + vnp13file, mode='r')

    name1 = '/HDFEOS/GRIDS/VIIRS_Grid_16Day_VI_500m/Data Fields/500 m 16 days NDVI'
    name2 = '/HDFEOS/GRIDS/VIIRS_Grid_16Day_VI_500m/Data Fields/500 m 16 days EVI'
    name3 = '/HDFEOS/GRIDS/VIIRS_Grid_16Day_VI_500m/Data Fields/500 m 16 days EVI2'

    data1 = np.array(f[name1][:]).astype(np.float64)
    data2 = np.array(f[name2][:]).astype(np.float64)
    data3 = np.array(f[name3][:]).astype(np.float64)

    # Read metadata.
    gridmeta = f['/HDFEOS INFORMATION/StructMetadata.0'][()]
    s = gridmeta.decode('UTF-8')
    f.close()

    # Construct the grid
    ul_regex = re.compile(
        r'''UpperLeftPointMtrs=\((?P<upper_left_x>[+-]?\d+\.\d+),(?P<upper_left_y>[+-]?\d+\.\d+)\)''', re.VERBOSE)
    match = ul_regex.search(s)
    x0 = np.float64(match.group('upper_left_x'))
    y0 = np.float64(match.group('upper_left_y'))
    lr_regex = re.compile(r'''LowerRightMtrs=\(
    (?P<lower_right_x>[+-]?\d+\.\d+)
    ,
    (?P<lower_right_y>[+-]?\d+\.\d+)
    \)''', re.VERBOSE)
    match = lr_regex.search(s)
    x1 = np.float64(match.group('lower_right_x'))
    y1 = np.float64(match.group('lower_right_y'))
    ny, nx = data1.shape
    x = np.linspace(x0, x1, nx, endpoint=False)
    y = np.linspace(y0, y1, ny, endpoint=False)
    xv, yv = np.meshgrid(x, y)

    sinu = pyproj.Proj("+proj=sinu +R=6371007.181 +nadgrids=@null +wktext")
    wgs84 = pyproj.Proj("+init=EPSG:4326")
    lon, lat = pyproj.transform(sinu, wgs84, xv, yv)

    return lon, lat, data1, data2, data3


def project_vi(abox, lat, lon, data1, data2, data3):
    # abox = [WestBoundingCoordinate, SouthBoundingCoordinate, EastBoundingCoordinate, NorthBoundingCoordinate
    SouthBoundingCoordinate = abox[1]
    NorthBoundingCoordinate = abox[3]
    WestBoundingCoordinate = abox[0]
    EastBoundingCoordinate = abox[2]

    # Target grid
    # target_nx = int((EastBoundingCoordinate - WestBoundingCoordinate) / 0.005)
    # target_ny = int((NorthBoundingCoordinate -
    #                 SouthBoundingCoordinate) / 0.005)
    
    target_nx = 166
    target_ny = 125
    
    # print(target_ny)
    source_cs = ccrs.PlateCarree()
    target_proj = ccrs.PlateCarree()

    target_lon = np.linspace(WestBoundingCoordinate,
                             EastBoundingCoordinate, target_nx)
    target_lat = np.linspace(NorthBoundingCoordinate,
                             SouthBoundingCoordinate, target_ny)
    target_lon2d, target_lat2d = np.meshgrid(target_lon, target_lat)

    # Perform regrid
    print('regrid')
    new_data1 = im_trans.regrid(data1, lon, lat, source_cs,
                                target_proj, target_lon2d, target_lat2d)

    new_data2 = im_trans.regrid(data2, lon, lat, source_cs,
                                target_proj, target_lon2d, target_lat2d)

    new_data3 = im_trans.regrid(data3, lon, lat, source_cs,
                                target_proj, target_lon2d, target_lat2d)

    return new_data1, new_data2, new_data3


for year in range(2023, 2024):
    year = str(year)
    start_doy = start_doy_dict[year]
    for doy in range(int(start_doy), 366, 8):
        doy = str(doy).zfill(3)
        logging.info(year + ' ' + doy)

        # load VNP13 HW part-1
        vnp13path1 = '/net/airs1/storage/people/mgcy/Data/VIIRS_VNP13A1_HW/VNP13A1/' + \
            year + '/' + str(doy)
        try:
            vnp13file1 = os.listdir(vnp13path1)
        except:
            logging.info('VNP13 Part-1 Missing @ ' + doy)
            continue

        # load VNP13 HW part-1
        vnp13path2 = '/net/airs1/storage/people/mgcy/Data/VIIRS_VNP13A1_HW_plus/VNP13A1/' + \
            year + '/' + str(doy)
        try:
            vnp13file2 = os.listdir(vnp13path2)
        except:
            logging.info('VNP13 Part-1 Missing @ ' + doy)
            continue

        # if file exists
        if len(vnp13file1) != 1 or len(vnp13file2) != 1:
            logging.info('VNP13 not one file @ ' + doy)
            continue
        elif str(doy) not in vnp13file1[0] or str(doy) not in vnp13file2[0]:
            logging.info('VNP13 DOY mis-mismatch @ ' + doy)
            continue
        else:
            lon1, lat1, ndvi_raw1, evi_raw1, evi2_raw1 = get_rad_lat_lon(
                vnp13path1, vnp13file1[0])
            lon2, lat2, ndvi_raw2, evi_raw2, evi2_raw2 = get_rad_lat_lon(
                vnp13path2, vnp13file2[0])

            lon = np.concatenate((lon1, lon2), axis=0)
            lat = np.concatenate((lat1, lat2), axis=0)

            ndvi_raw = np.concatenate((ndvi_raw1, ndvi_raw2), axis=0) / 10000.0
            evi_raw = np.concatenate((evi_raw1, evi_raw2), axis=0) / 10000.0
            evi2_raw = np.concatenate((evi2_raw1, evi2_raw2), axis=0) / 10000.0

            # plt.imshow(ndvi_raw)
            # plt.savefig('ndvi.tmp.png')

            vi_list = []
            for Island in Island_list:
                abox = Island_abox[Island]
                new_ndvi, new_evi, new_evi2 = project_vi(
                    abox, lat, lon, ndvi_raw, evi_raw, evi2_raw)
                tmp_array = np.array([new_ndvi, new_evi, new_evi2])
                # print(tmp_array.shape)
                vi_list.append(tmp_array)
                
                
                # plt.figure()
                # plt.imshow(new_ndvi)
                # print(new_ndvi.shape)
                # plt.savefig('ndvi ' + Island + '.tmp.png')
            
            vi_all = np.array(vi_list)
            
            vi_all[vi_all==-1.5] = 0
            vi_all[vi_all>=1] = 1
            vi_all[vi_all<=-1] = -1
                
            print(vi_all.shape)
            # np.save(savepath + 'tmp.npy', vi_all)
            np.save(savepath + 'VIIRS.VNP13.VI.Test.' + year +
                    '.' + str(doy) + '.npy', vi_all)
