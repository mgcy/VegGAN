import numpy as np
import h5py
import matplotlib.pyplot as plt


import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import cartopy.feature as cf

import matplotlib.ticker as mticker
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER

workpath = '/net/airs1/storage/people/mgcy/Projects/VIIRS_Super_Resolution/'

def plot_function(viirs, landsat, ftype, fdate):
    states_provinces = cf.NaturalEarthFeature(
    category='cultural',
    name='admin_1_states_provinces_lines',
    scale='50m',
    facecolor='none')

    abox = [-156.75, 20.45, -155.95, 21.05]

    area2 = [-156.75, -155.95, 20.45,  21.05]
    
    fig = plt.figure(figsize=[10, 4])
    ax1 = fig.add_subplot(1, 2, 1, projection=ccrs.PlateCarree())
    ax2 = fig.add_subplot(1, 2, 2, projection=ccrs.PlateCarree())

    # ---------
    #   VIIRS
    # ---------

    lon = np.linspace(start=abox[0], stop=abox[2], num=viirs.shape[1])
    lat = np.linspace(start=abox[1], stop=abox[3], num=viirs.shape[0])
    lon, lat = np.meshgrid(lon, lat)

    ax1.set_title("(a) Original Landsat " + ftype)

    ax1.add_feature(states_provinces, edgecolor='black', linewidth=2.5, zorder=3)
    # ax1.add_feature(cf.LAND)
    ax1.add_feature(cf.OCEAN, zorder=3, color='white')
    ax1.add_feature(cf.COASTLINE, linewidth=2.5, zorder=4)
    # ax1.add_feature(cf.BORDERS, linestyle=':')

    ax1.pcolormesh(lon, lat, np.flipud(viirs), cmap='RdYlGn', transform=ccrs.PlateCarree(), vmax=1, vmin=-1, rasterized=True)

    gls = ax1.gridlines(draw_labels=False, crs=ccrs.PlateCarree(), linestyle='--', zorder=4)

    # ax1.coastlines()

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
    #  Landsat
    # ---------

    lon = np.linspace(start=abox[0], stop=abox[2], num=landsat.shape[1])
    lat = np.linspace(start=abox[1], stop=abox[3], num=landsat.shape[0])
    lon, lat = np.meshgrid(lon, lat)

    ax2.set_title("(b) MVC Landsat " + ftype)

    ax2.add_feature(cf.OCEAN, zorder=3, color='white')
    ax2.add_feature(cf.COASTLINE, linewidth=2.5, zorder=4)

    cm = ax2.pcolormesh(lon, lat, np.flipud(landsat), cmap='RdYlGn', transform=ccrs.PlateCarree(), vmax=1, vmin=-1, rasterized=True)

    gls = ax2.gridlines(draw_labels=False, crs=ccrs.PlateCarree(), linestyle='--', zorder=4)

    # ax2.coastlines()

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

    ax1.plot([area2[1], area2[1], area2[0], area2[0], area2[1]], [area2[2], area2[3], area2[3], area2[2], area2[2]],
         color='black', linewidth=1, zorder = 5, 
         transform=ccrs.PlateCarree())
    
    ax2.plot([area2[1], area2[1], area2[0], area2[0], area2[1]], [area2[2], area2[3], area2[3], area2[2], area2[2]],
         color='black', linewidth=1, zorder = 5, 
         transform=ccrs.PlateCarree())
    
    
    cbaxes = fig.add_axes([0.92, 0.15, 0.01, 0.65])  # [left, bottom, width, height]
    cb = fig.colorbar(cm, cax=cbaxes)
    cb.set_label(ftype, fontsize=14)


    plt.savefig(workpath + '/Plots/MVC/'  + fdate + '.' + ftype + ".pdf", format='pdf',
            bbox_inches='tight', facecolor=(1, 1, 1, 0))
    plt.close()

 

landsat_start_doy_dict = {'2018':'13',
                  '2019':'16',
                  '2020':'3',
                  '2021':'5',
                  '2022':'8',
                  '2023':'11',}

for year in range(2018, 2024):
    year = str(year)
    doy = int(landsat_start_doy_dict[year])
    while int(doy) <= 365:
        doy = str(doy).zfill(3)
        try:
            landsat_mvc = np.load(workpath + 'Landsat_VI_MVC_HW/Landsat.VI.MVC.' + year + '.' + str(doy) + '.npy')[0]
            landsat_tmp = np.load(workpath + 'Landsat_VI_HW/Landsat.VI.' + year + '.' + str(doy) + '.npy')[0] 
            
            landsat_tmp[landsat_tmp<=0.1] = 0
            landsat_mvc[landsat_mvc<=0.1] = 0
            
            plot_function(landsat_tmp, landsat_mvc, ftype="NDVI", fdate = year + '.' + str(doy))
              
        except: 
            print('Missing ', year, doy)
        doy = int(doy) + 16

# plot_test_example_HW(filelist[0][3:11])

