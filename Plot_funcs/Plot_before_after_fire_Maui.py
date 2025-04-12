import numpy as np
import h5py
import matplotlib.pyplot as plt


import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import cartopy.feature as cf

import matplotlib.ticker as mticker
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER

workpath = '/net/airs1/storage/people/mgcy/Projects/VIIRS_Super_Resolution/'

def plot_function(viirs, sr, ftype, fdate, date):
    states_provinces = cf.NaturalEarthFeature(
    category='cultural',
    name='admin_1_states_provinces_lines',
    scale='50m',
    facecolor='none')

    abox = [-156.75, 20.45, -155.95, 21.05]

    fig = plt.figure(figsize=[10, 4])
    ax1 = fig.add_subplot(1, 2, 1, projection=ccrs.PlateCarree())
    ax2 = fig.add_subplot(1, 2, 2, projection=ccrs.PlateCarree())

    # ---------
    #   VIIRS
    # ---------

    lon = np.linspace(start=abox[0], stop=abox[2], num=viirs.shape[1])
    lat = np.linspace(start=abox[1], stop=abox[3], num=viirs.shape[0])
    lon, lat = np.meshgrid(lon, lat)

    ax1.set_title("(a) VIIRS " + ftype + ' on ' + date)

    ax1.add_feature(states_provinces, edgecolor='black', linewidth=2.5, zorder=3)
    ax1.add_feature(cf.LAND)
    ax1.add_feature(cf.OCEAN, zorder=3)
    ax1.add_feature(cf.COASTLINE, linewidth=2.5)
    ax1.add_feature(cf.BORDERS, linestyle=':')

    ax1.pcolormesh(lon, lat, np.flipud(viirs), cmap='RdYlGn', transform=ccrs.PlateCarree(), vmax=1, vmin=-1, rasterized=True)

    gls = ax1.gridlines(draw_labels=False, crs=ccrs.PlateCarree(), linestyle='--', zorder=4)

    ax1.coastlines()

    x = np.round(np.linspace(lon.min(), lon.max(), 5), 2)
    y = np.round(np.linspace(lat.min(), lat.max(), 4), 2)

    gls.xlocator = mticker.FixedLocator(x)
    gls.ylocator = mticker.FixedLocator(y)

    ax1.set_xticks(x)
    ax1.set_yticks(y)
    ax1.set_xlim(lon.min(), lon.max())
    ax1.set_ylim(lat.min(), lat.max())
    ax1.set_xlabel('Longitude')
    ax1.set_ylabel('Latitude')

    # ---------
    #  SR
    # ---------

    lon = np.linspace(start=abox[0], stop=abox[2], num=sr.shape[1])
    lat = np.linspace(start=abox[1], stop=abox[3], num=sr.shape[0])
    lon, lat = np.meshgrid(lon, lat)

    ax2.set_title("(b) SR " + ftype + ' on ' + date)

    ax2.add_feature(states_provinces, edgecolor='black', linewidth=2.5, zorder=3)
    ax2.add_feature(cf.LAND)
    ax2.add_feature(cf.OCEAN, zorder=3)
    ax2.add_feature(cf.COASTLINE, linewidth=2.5)
    ax2.add_feature(cf.BORDERS, linestyle=':')

    cm = ax2.pcolormesh(lon, lat, np.flipud(sr), cmap='RdYlGn', transform=ccrs.PlateCarree(), vmax=1, vmin=-1, rasterized=True)

    gls = ax2.gridlines(draw_labels=False, crs=ccrs.PlateCarree(), linestyle='--', zorder=4)

    ax2.coastlines()

    x = np.round(np.linspace(lon.min(), lon.max(), 5), 2)
    y = np.round(np.linspace(lat.min(), lat.max(), 4), 2)

    gls.xlocator = mticker.FixedLocator(x)
    gls.ylocator = mticker.FixedLocator(y)

    ax2.set_xticks(x)
    ax2.set_yticks(y)
    ax2.set_xlim(lon.min(), lon.max())
    ax2.set_ylim(lat.min(), lat.max())
    ax2.set_xlabel('Longitude')
    ax2.set_ylabel('Latitude')

    cbaxes = fig.add_axes([0.92, 0.12, 0.01, 0.75])  # [left, bottom, width, height]
    cb = fig.colorbar(cm, cax=cbaxes)
    cb.set_label(ftype, fontsize=14)


    plt.savefig(workpath + '/Plots/Fire_eg/'  + fdate + '.' + ftype + ".png", format='png',
            bbox_inches='tight', facecolor=(1, 1, 1, 0))
    plt.close()


def plot_test_example_HW(filedate, date):
    hr_height = 2000
    hr_width = 2656
    # load sr outputs
    filename = workpath + 'Results/Variables/Test_SR_HW/VI.' + filedate + '.HW.npy'
    sr = np.load(filename, allow_pickle=True)
    sr_ndvi = sr[0, :hr_height, :hr_width]


    # load landsat and viirs
    filename = workpath + 'ML_VI_MVC_Data_HW/Test/VI.' + filedate + '.HW.h5'
    file = h5py.File(filename, 'r')
    viirs = np.array(file['viirs'][:])
    file.close()

    viirs_ndvi = viirs[0]

    # load mask
    y_mask = np.load(workpath + 'Masks/Mask.30m.npy')
    y_mask[y_mask == 0 ] = np.nan
    x_mask = np.load(workpath + 'Masks/Mask.480m.npy')
    x_mask[x_mask == 0 ] = np.nan

    # apply mask
    sr_ndvi *= y_mask

    viirs_ndvi *= x_mask


    plot_function(viirs_ndvi, sr_ndvi, ftype="NDVI", fdate = filedate, date=date)


    
import os
filelist = os.listdir(workpath + 'Results/Variables/Test_SR_HW/')

# plot_test_example_HW(filelist[0][3:11])
filelist=['VI.2023.219.HW.h5', 'VI.2023.267.HW.h5']
datelist = ['Aug 7, 2023','Sep 24, 2023']
i=0
for filename in filelist:
    filedate = filename[3:11]
    print(filedate)
    plot_test_example_HW(filedate, datelist[i])
    i+=-1
