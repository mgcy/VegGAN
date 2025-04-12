import rioxarray as rxr
import glob
import os
from datetime import datetime
import logging
from rasterio.crs import CRS
import cv2
import numpy as np
import json

logging.basicConfig(filename="Proj.Landsat.log", level=logging.INFO,
                    format='%(asctime)s %(message)s',
                    filemode='w')

# savepath = '/net/airs1/storage/people/mgcy/Projects/VIIRS_Super_Resolution/Landsat_VI_CO/' # CO
savepath = '/net/airs1/storage/people/mgcy/Projects/VIIRS_Super_Resolution/Landsat_VI_HW/'   # HW

def calculate_reflectance(img, E, MR=2e-5, AR=-0.1):
    rf = ((MR * img.astype(np.float32)) + AR) / np.sin(np.deg2rad(E))
    return rf

def cal_doy(date):
    # d must in "monthdayyear" format, e.g., d="20181225"
    year = date[0:4]
    month = date[4:6]
    day = date[6:8]
    d = year + '-' + month + '-' + day
    start_day_of_year = datetime.strptime(year + '-1-1', "%Y-%m-%d")
    d = datetime.strptime(d, "%Y-%m-%d")
    day_tmp = abs((d - start_day_of_year).days) + 1
    if day_tmp < 10:
        day_re = '00' + str(day_tmp)
    elif day_tmp < 100:
        day_re = '0' + str(day_tmp)
    else:
        day_re = str(day_tmp)
    return day_re


for year in range(2023,2024):
    year = str(year)
    
    # datapath = '/net/airs1/storage/people/mgcy/Projects/VIIRS_Super_Resolution/Landsat_CO_untar/' + year + '/'      # CO
    datapath = '/net/airs1/storage/people/mgcy/Projects/VIIRS_Super_Resolution/Landsat_HW_untar/' + year + '/'    # HW
    subfolders = os.listdir(datapath)
    subfolders.sort()
    
    for subfolder in subfolders:
        date = subfolder[17:25]
        doy = cal_doy(date)
        logging.info('Found @ ' + year + '-' + doy)
        
        red_filename = glob.glob(datapath + subfolder + '/*_B4.TIF')[0]
        nir_filename = glob.glob(datapath + subfolder + '/*_B5.TIF')[0]
        blue_filename = glob.glob(datapath + subfolder + '/*_B2.TIF')[0]
        mtl_filename = glob.glob(datapath + subfolder + '/*_MTL.json')[0]
        
        try: 
            # load three channels
            red = rxr.open_rasterio(red_filename, masked=True).squeeze()
            nir = rxr.open_rasterio(nir_filename, masked=True).squeeze()
            blue = rxr.open_rasterio(blue_filename, masked=True).squeeze()
            
            nir = nir.rio.reproject(CRS.from_epsg(4326))
            red = red.rio.reproject(CRS.from_epsg(4326))
            blue = blue.rio.reproject(CRS.from_epsg(4326))
            
            # CO
            # min_lon = -106.50
            # min_lat = 40.00
            # max_lon = min_lon + 0.8
            # max_lat = min_lat + 0.8

            # HW
            min_lon = -156.75
            min_lat = 20.45
            max_lon = -155.95
            max_lat = 21.05
            
            nir = nir.rio.clip_box(minx=min_lon, miny=min_lat, maxx=max_lon, maxy=max_lat)
            red = red.rio.clip_box(minx=min_lon, miny=min_lat, maxx=max_lon, maxy=max_lat)
            blue = blue.rio.clip_box(minx=min_lon, miny=min_lat, maxx=max_lon, maxy=max_lat)
            
            # datasize = (640, 640)   # CO 125m
            # datasize = (640, 480)   # HW 125 m
            datasize = (2656, 2000) # HW 30m
            
            nir = cv2.resize(np.array(nir), dsize=datasize, interpolation=cv2.INTER_CUBIC)
            red = cv2.resize(np.array(red), dsize=datasize, interpolation=cv2.INTER_CUBIC)
            blue = cv2.resize(np.array(blue), dsize=datasize, interpolation=cv2.INTER_CUBIC)
            
            # load sun elevation
            mtl_file = json.load(open(mtl_filename))
            elevation = float(mtl_file['LANDSAT_METADATA_FILE']['IMAGE_ATTRIBUTES']['SUN_ELEVATION'])
            
            # convert to reflectance
            nir = calculate_reflectance(nir, elevation)
            red = calculate_reflectance(red, elevation)
            blue = calculate_reflectance(blue, elevation)
            
            # calculate VI
            ndvi = (nir - red) / (nir + red)
            evi = 2.5 * ((nir - red) / (nir + 6 * red - 7.5 * blue + 1))
            evi2 = 2.5 * ((nir - red) / (nir + 2.4 * red + 1))
            
           # save data 
            vi_stack = np.stack((ndvi, evi, evi2), axis=0)
            np.save(savepath + 'Landsat.VI.' + year + '.' + str(doy) + '.npy', vi_stack)
            
        except:
            logging.info('Warning: Failure @ ' + year + '-' + doy)
