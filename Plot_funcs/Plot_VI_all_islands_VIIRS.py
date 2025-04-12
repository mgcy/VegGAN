import os
import re
import h5py
import pyproj
import cartopy.img_transform as im_trans
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

workpath = '/net/airs1/storage/people/mgcy/Projects/VIIRS_Super_Resolution/'
import os
import re
import h5py
import pyproj
import cartopy.img_transform as im_trans
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import warnings
import numpy as np
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import cartopy.feature as cf

import matplotlib.ticker as mticker
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import cartopy.mpl.ticker as cticker

warnings.filterwarnings('ignore')

def get_rad_lat_lon(FILE_NAME, GRID_NAME = 'GRID_NAME', DATAFIELD_NAME = 'SurfReflect_I1_1'):

    datapath = '/net/airs1/storage/people/mgcy/Data/'

    # FILE_NAME = workpath + 'VNP13A1.A2023233.h03v06.002.2023251191441.h5'
    # GRID_NAME = 'VIIRS_Grid_500m_2D'
    # DATAFIELD_NAME = 'SurfReflect_I1_1'

    f = h5py.File(datapath + FILE_NAME, mode='r')
    name = '/HDFEOS/GRIDS/{0}/Data Fields/{1}'.format(GRID_NAME, DATAFIELD_NAME)
    data = np.array(f[name][:]).astype(np.float64)

    # Read metadata.
    gridmeta = f['/HDFEOS INFORMATION/StructMetadata.0'][()]
    s = gridmeta.decode('UTF-8')

    # Construct the grid.  The needed information is in a string dataset
    # called 'StructMetadata.0'.  Use regular expressions to retrieve
    # extents of the grid.
    ul_regex = re.compile(r'''UpperLeftPointMtrs=\((?P<upper_left_x>[+-]?\d+\.\d+),(?P<upper_left_y>[+-]?\d+\.\d+)\)''', re.VERBOSE)
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

filename1 = 'VIIRS_VNP13A1_HW/VNP13A1/2023/193/VNP13A1.A2023193.h03v06.002.2023242141854.h5'
filename2 = 'VIIRS_VNP13A1_HW_plus/VNP13A1/2023/193/VNP13A1.A2023193.h03v07.002.2023242141851.h5'
lon1_p1, lat1_p1, ndvi_raw_p1 = get_rad_lat_lon(filename1, 'VIIRS_Grid_16Day_VI_500m', '500 m 16 days EVI2')
lon1_p2, lat1_p2, ndvi_raw_p2 = get_rad_lat_lon(filename2, 'VIIRS_Grid_16Day_VI_500m', '500 m 16 days EVI2')

lon_1 = np.concatenate((lon1_p1, lon1_p2), axis = 0)
lat_1 = np.concatenate((lat1_p1, lat1_p2), axis = 0)


ndvi_raw = np.concatenate((ndvi_raw_p1, ndvi_raw_p2), axis = 0) /10000.0

import cartopy.crs as ccrs
SouthBoundingCoordinate = 18.85
NorthBoundingCoordinate = 22.35
WestBoundingCoordinate = -160.3
EastBoundingCoordinate = -154.7

# Target grid
target_nx = int((EastBoundingCoordinate - WestBoundingCoordinate) / 0.0048)
target_ny = int((NorthBoundingCoordinate - SouthBoundingCoordinate) / 0.0048)
source_cs = ccrs.Geodetic()
target_proj = ccrs.PlateCarree()
print('Trans x y')

target_lon = np.linspace(WestBoundingCoordinate, EastBoundingCoordinate, target_nx)
target_lat = np.linspace(NorthBoundingCoordinate, SouthBoundingCoordinate, target_ny)
target_lon2d, target_lat2d = np.meshgrid(target_lon, target_lat)

# Perform regrid
print('regrid')
ndvi = im_trans.regrid(ndvi_raw, lon_1, lat_1, source_cs,
                            target_proj, target_lon2d, target_lat2d)


def plot_data(data):
    states_provinces = cf.NaturalEarthFeature(
        category='cultural',
        name='admin_1_states_provinces_lines',
        scale='50m',
        facecolor='none')

    abox = [WestBoundingCoordinate, SouthBoundingCoordinate, EastBoundingCoordinate, NorthBoundingCoordinate]
    lon = np.linspace(start=abox[0], stop=abox[2], num=data.shape[1])
    lat = np.linspace(start=abox[1], stop=abox[3], num=data.shape[0])
    lon, lat = np.meshgrid(lon, lat)

    fig = plt.figure(figsize=[14, 5])
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
    ax.set_title('(a) VIIRS EVI2')
    ax.add_feature(states_provinces, edgecolor='gray')
    ax.add_feature(cf.LAND)
    ax.add_feature(cf.OCEAN, zorder = 3)
    ax.add_feature(cf.COASTLINE, linewidth=2.5)
    ax.add_feature(cf.BORDERS, linestyle=':')

    cm = ax.imshow(data, extent=(-160.3, -154.7, 18.85, 22.35), cmap='RdYlGn', transform=ccrs.PlateCarree(), vmax=1, vmin=-1, rasterized=True)


    cbar = plt.colorbar(cm, aspect=35, pad=0.01)
    cbar.set_label('EVI2')

    gls = ax.gridlines(draw_labels=False, crs=ccrs.PlateCarree(), linestyle='--')

    ax.coastlines()
    x = np.round(np.linspace(lon.min(), lon.max(), 5), 2)
    y = np.round(np.linspace(lat.min(), lat.max(), 4), 2)

    gls.xlocator = mticker.FixedLocator(x)
    gls.ylocator = mticker.FixedLocator(y)

    ax.set_xticks(x)
    ax.set_yticks(y)
    ax.set_xlim(lon.min(), lon.max())
    ax.set_ylim(lat.min(), lat.max())
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    plt.savefig(workpath + '/Plots/All_Islands/VIIRS.EVI2.All.Islands.png', bbox_inches='tight', facecolor=(1, 1, 1, 0))
    plt.close()

print(ndvi.shape)
plot_data(ndvi)


# np.save('All_Islands.NDVI.npy', ndvi)
