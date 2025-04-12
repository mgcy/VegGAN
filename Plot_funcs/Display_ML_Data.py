import os
import numpy as np
import matplotlib.pyplot as plt
import netCDF4 as nc
from cartopy import crs as ccrs
import cartopy.img_transform as im_trans

viirspath = '/net/airs1/storage/people/mgcy/Projects/VIIRS_Super_Resolution/VIIRS_NDVI/'
landsatpath = '/net/airs1/storage/people/mgcy/Projects/VIIRS_Super_Resolution/Landsat_NDVI/'

year = '2015'
doy = '218'


vnp02path = '/net/airs1/storage/people/mgcy/Data/VIIRS_CO_raw/VNP02IMG/' + \
            year + '/' + str(doy)
vnp02file = os.listdir(vnp02path)
NC = nc.Dataset(vnp02path + '/' + vnp02file[0])
obv_data = NC.groups['observation_data']
nir_data_sr = np.array(obv_data.variables['I02'][:])
red_data_sr = np.array(obv_data.variables['I01'][:])

vnp03path = '/net/airs1/storage/people/mgcy/Data/VIIRS_CO_raw/VNP03IMG/' + \
            year + '/' + str(doy)
vnp03file = os.listdir(vnp03path)
NC = nc.Dataset(vnp03path + '/' + vnp03file[0])
geo_data = NC.groups['geolocation_data']
lat = np.array(geo_data.variables['latitude'][:])
lon = np.array(geo_data.variables['longitude'][:])

# reprojection
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
nir_data_proj = im_trans.regrid(nir_data_sr, lon, lat, source_cs,
                                target_proj, target_lon2d, target_lat2d)
red_data_proj = im_trans.regrid(red_data_sr, lon, lat, source_cs,
                                target_proj, target_lon2d, target_lat2d)

# load NDVI
viirs_ndvi = np.load(viirspath + 'VIIRS.NDVI.' + year + '.' + str(doy) + '.npy')         
landsat_ndvi = np.load(landsatpath + 'Landsat.NDVI.' + year + '.' + str(doy) + '.npy')

fig, axes = plt.subplots(2,2, figsize=(16,16))

im1 = axes[0,0].imshow(nir_data_proj)
axes[0,0].set_title('VIIRS NIR')
plt.colorbar(im1, fraction=0.04, pad=0.025)

im2 = axes[0,1].imshow(red_data_proj)
axes[0,1].set_title('VIIRS RED')
plt.colorbar(im2, fraction=0.04, pad=0.025)

# im1 = axes[1,0].imshow(nir_data_sr[:,2100:4200], cmap='RdYlGn')
im1 = axes[1,0].imshow(lon, cmap='RdYlGn')

axes[1,0].set_title('VIIRS NDVI')
plt.colorbar(im1, fraction=0.04, pad=0.025)

# im2 = axes[1,1].imshow(red_data_sr[:,2100:4200], cmap='RdYlGn')
im2 = axes[1,1].imshow(lat, cmap='RdYlGn')

axes[1,1].set_title('Landsat NDVI')
plt.colorbar(im2, fraction=0.04, pad=0.025)

plt.savefig('Eg.' + year + '.' + doy + '.png', format='png',
            bbox_inches='tight')