import cartopy
import numpy as np
import os
from cartopy import crs as ccrs
import cartopy.img_transform as im_trans
import logging
import h5py
import re
import pyproj
import warnings
warnings.filterwarnings('ignore')

logging.basicConfig(filename="Proj.VIIRS.log", level=logging.INFO,
                    format='%(asctime)s %(message)s',
                    filemode='w')

# savepath = '/net/airs1/storage/people/mgcy/Projects/VIIRS_Super_Resolution/VIIRS_VI_CO/' # CO
savepath = '/net/airs1/storage/people/mgcy/Projects/VIIRS_Super_Resolution/VIIRS_VI_HW/' # HW

start_doy_dict = {'2018': '9',
                  '2019': '1',
                  '2020': '1',
                  '2021': '1',
                  '2022': '1',
                  '2023': '1', }


def get_rad_lat_lon(f, GRID_NAME, DATAFIELD_NAME):

    name = '/HDFEOS/GRIDS/{0}/Data Fields/{1}'.format(GRID_NAME,
                                                      DATAFIELD_NAME)
    data = np.array(f[name][:]).astype(np.float64)

    # Read metadata.
    gridmeta = f['/HDFEOS INFORMATION/StructMetadata.0'][()]
    s = gridmeta.decode('UTF-8')

    # Construct the grid.  The needed information is in a string dataset
    # called 'StructMetadata.0'.  Use regular expressions to retrieve
    # extents of the grid.
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
    ny, nx = data.shape
    x = np.linspace(x0, x1, nx, endpoint=False)
    y = np.linspace(y0, y1, ny, endpoint=False)
    xv, yv = np.meshgrid(x, y)

    sinu = pyproj.Proj("+proj=sinu +R=6371007.181 +nadgrids=@null +wktext")
    wgs84 = pyproj.Proj("+init=EPSG:4326")
    lon, lat = pyproj.transform(sinu, wgs84, xv, yv)

    return lon, lat, data


for year in range(2023, 2024):
    year = str(year)
    start_doy = start_doy_dict[year]
    for doy in range(int(start_doy), 366, 8):
        doy = str(doy).zfill(3)
        logging.info(year + ' ' + doy)

        # load VNP13 CO
        # vnp13path = '/net/airs1/storage/people/mgcy/Data/VIIRS_VNP13A1_CO/VNP13A1/' + \
        #     year + '/' + str(doy)
        # load VNP13 HW    
        vnp13path = '/net/airs1/storage/people/mgcy/Data/VIIRS_VNP13A1_HW/VNP13A1/' + \
            year + '/' + str(doy)
        try:
            vnp13file = os.listdir(vnp13path)
        except:
            logging.info('VNP13 Missing @ ' + doy)
            continue

        # if file exists
        if len(vnp13file) != 1:
            logging.info('VNP13 not one file @ ' + doy)
            continue
        elif str(doy) not in vnp13file[0]:
            logging.info('VNP13 DOY mis-mismatch @ ' + doy)
            continue
        else:
            f = h5py.File(vnp13path + '/' + vnp13file[0], mode='r')

            lon1, lat1, ndvi_raw = get_rad_lat_lon(
                f, 'VIIRS_Grid_16Day_VI_500m', '500 m 16 days NDVI')
            lon2, lat2, evi_raw = get_rad_lat_lon(
                f, 'VIIRS_Grid_16Day_VI_500m', '500 m 16 days EVI')
            lon3, lat3, evi2_raw = get_rad_lat_lon(
                f, 'VIIRS_Grid_16Day_VI_500m', '500 m 16 days EVI2')

            # CO
            # SouthBoundingCoordinate = 40.0
            # NorthBoundingCoordinate = 40.8
            # WestBoundingCoordinate = -106.5
            # EastBoundingCoordinate = -105.7
            
            # HW
            SouthBoundingCoordinate = 20.45
            NorthBoundingCoordinate = 21.05
            WestBoundingCoordinate = -156.75
            EastBoundingCoordinate = -155.95

            # Target grid
            # target_nx = int(
            #     (EastBoundingCoordinate - WestBoundingCoordinate) / 0.005)
            # target_ny = int((NorthBoundingCoordinate -
            #                 SouthBoundingCoordinate) / 0.005)
            
            # Target grid
            target_nx = 166
            target_ny = 125
            
            source_cs = ccrs.Geodetic()
            target_proj = ccrs.PlateCarree()
            print('Trans x y')

            target_lon = np.linspace(
                WestBoundingCoordinate, EastBoundingCoordinate, target_nx)
            target_lat = np.linspace(
                NorthBoundingCoordinate, SouthBoundingCoordinate, target_ny)
            target_lon2d, target_lat2d = np.meshgrid(target_lon, target_lat)

            # Perform regrid
            print('regrid')
            ndvi = im_trans.regrid(ndvi_raw, lon1, lat1, source_cs,
                                   target_proj, target_lon2d, target_lat2d)

            evi = im_trans.regrid(evi_raw, lon2, lat2, source_cs,
                                  target_proj, target_lon2d, target_lat2d)

            evi2 = im_trans.regrid(evi2_raw, lon3, lat3, source_cs,
                                   target_proj, target_lon2d, target_lat2d)

            vi_stack = np.stack((ndvi, evi, evi2), axis=0)
            np.save(savepath + 'VIIRS.VNP13.VI.' + year +
                    '.' + str(doy) + '.npy', vi_stack)
