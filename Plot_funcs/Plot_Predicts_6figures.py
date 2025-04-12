import numpy as np
import h5py
import matplotlib.pyplot as plt

import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import cartopy.feature as cf

import matplotlib.ticker as mticker
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER

workpath = '/net/airs1/storage/people/mgcy/Projects/VIIRS_Super_Resolution/'

import matplotlib as mpl
mpl.rcParams['xtick.labelsize'] = 14
mpl.rcParams['ytick.labelsize'] = 14

def plot_function(viirs, landsat, sr, interpolation, ftype, fdate):
    abox = [-156.75, 20.45, -155.95, 21.05]
    area = [-156.34, -156.26, 20.85, 20.79]
    
    fig = plt.figure(figsize=[16, 8])
    ax1 = fig.add_subplot(2, 3, 1, projection=ccrs.PlateCarree())
    ax2 = fig.add_subplot(2, 3, 2, projection=ccrs.PlateCarree())
    ax3 = fig.add_subplot(2, 3, 3, projection=ccrs.PlateCarree())
    ax4 = fig.add_subplot(2, 3, 4, projection=ccrs.PlateCarree())
    ax5 = fig.add_subplot(2, 3, 5, projection=ccrs.PlateCarree())
    ax6 = fig.add_subplot(2, 3, 6, projection=ccrs.PlateCarree())

    # ---------
    #   VIIRS
    # ---------

    lon = np.linspace(start=abox[0], stop=abox[2], num=viirs.shape[1])
    lat = np.linspace(start=abox[1], stop=abox[3], num=viirs.shape[0])
    lon, lat = np.meshgrid(lon, lat)

    ax1.set_title("(a) VIIRS " + ftype, fontsize=18)
    ax1.add_feature(cf.COASTLINE, linewidth=2.5)

    ax1.pcolormesh(lon, lat, np.flipud(viirs), cmap='RdYlGn', transform=ccrs.PlateCarree(), vmax=1, vmin=-1, rasterized=True)

    gls = ax1.gridlines(draw_labels=False, crs=ccrs.PlateCarree(), linestyle='--', zorder=4)

    x = np.round(np.linspace(lon.min(), lon.max(), 5), 2)
    y = np.round(np.linspace(lat.min(), lat.max(), 4), 2)

    gls.xlocator = mticker.FixedLocator(x)
    gls.ylocator = mticker.FixedLocator(y)

    ax1.set_xticks(x)
    ax1.set_yticks(y)
    ax1.set_xlim(lon.min(), lon.max())
    ax1.set_ylim(lat.min(), lat.max())
    ax1.set_xlabel('Longitude', fontsize=16)
    ax1.set_ylabel('Latitude', fontsize=16)
    
    ax1.plot([area[1], area[1], area[0], area[0], area[1]], [area[2], area[3], area[3], area[2], area[2]],
         color='blue', linewidth=2,
         transform=ccrs.PlateCarree())
    

    # ---------
    #  Landsat
    # ---------

    lon = np.linspace(start=abox[0], stop=abox[2], num=landsat.shape[1])
    lat = np.linspace(start=abox[1], stop=abox[3], num=landsat.shape[0])
    lon, lat = np.meshgrid(lon, lat)

    ax2.set_title("(b) Landsat " + ftype, fontsize=18)
    ax2.add_feature(cf.COASTLINE, linewidth=2.5)

    ax2.pcolormesh(lon, lat, np.flipud(landsat), cmap='RdYlGn', transform=ccrs.PlateCarree(), vmax=1, vmin=-1, rasterized=True)
    gls = ax2.gridlines(draw_labels=False, crs=ccrs.PlateCarree(), linestyle='--', zorder=4)
    
    x = np.round(np.linspace(lon.min(), lon.max(), 5), 2)
    y = np.round(np.linspace(lat.min(), lat.max(), 4), 2)

    gls.xlocator = mticker.FixedLocator(x)
    gls.ylocator = mticker.FixedLocator(y)

    ax2.set_xticks(x)
    ax2.set_yticks(y)
    ax2.set_xlim(lon.min(), lon.max())
    ax2.set_ylim(lat.min(), lat.max())
    ax2.set_xlabel('Longitude', fontsize=16)
    ax2.set_ylabel('Latitude', fontsize=16)
    ax2.plot([area[1], area[1], area[0], area[0], area[1]], [area[2], area[3], area[3], area[2], area[2]],
         color='orange', linewidth=2,
         transform=ccrs.PlateCarree())
    
    # ---------
    #    SR
    # ---------
    ax3.set_title("(c) Downscaled VIIRS " + ftype, fontsize=18)
    ax3.add_feature(cf.COASTLINE, linewidth=2.5)
    
    ax3.pcolormesh(lon, lat, np.flipud(sr), cmap='RdYlGn', transform=ccrs.PlateCarree(), vmax=1, vmin=-1, rasterized=True)
    gls = ax3.gridlines(draw_labels=False, crs=ccrs.PlateCarree(), linestyle='--', zorder=4)
    
    x = np.round(np.linspace(lon.min(), lon.max(), 5), 2)
    y = np.round(np.linspace(lat.min(), lat.max(), 4), 2)
    
    gls.xlocator = mticker.FixedLocator(x)
    gls.ylocator = mticker.FixedLocator(y)
    
    ax3.set_xticks(x)
    ax3.set_yticks(y)
    ax3.set_xlim(lon.min(), lon.max())
    ax3.set_ylim(lat.min(), lat.max())
    ax3.set_xlabel('Longitude', fontsize=16)
    ax3.set_ylabel('Latitude', fontsize=16)
    ax3.plot([area[1], area[1], area[0], area[0], area[1]], [area[2], area[3], area[3], area[2], area[2]],
         color='red', linewidth=2,
         transform=ccrs.PlateCarree())
    
    # ---------
    #    VIIRS Zoomin
    # ---------
    
    lon = np.linspace(start=abox[0], stop=abox[2], num=viirs.shape[1])
    lat = np.linspace(start=abox[1], stop=abox[3], num=viirs.shape[0])
    lon, lat = np.meshgrid(lon, lat)

    ax4.set_title("(d) Zoomed VIIRS " + ftype, fontsize=18)
    ax4.set_extent(area, crs=ccrs.PlateCarree())
    ax4.add_feature(cf.COASTLINE, linewidth=2.5)
    ax4.pcolormesh(lon, lat, np.flipud(viirs), cmap='RdYlGn', transform=ccrs.PlateCarree(), vmax=1, vmin=-1, rasterized=True)
    gls = ax4.gridlines(draw_labels=False, crs=ccrs.PlateCarree(), linestyle='--', zorder=4)
    x = np.round(np.linspace(area[0], area[1], 3), 2)
    y = np.round(np.linspace(area[2], area[3], 3), 2)
    gls.xlocator = mticker.FixedLocator(x)
    gls.ylocator = mticker.FixedLocator(y)
    ax4.set_xticks(x)
    ax4.set_yticks(y)
    ax4.set_xlabel('Longitude', fontsize=16)
    ax4.set_ylabel('Latitude', fontsize=16)
    ax4.plot([area[1], area[1], area[0], area[0], area[1]], [area[2], area[3], area[3], area[2], area[2]],
         color='blue', linewidth=6,
         transform=ccrs.PlateCarree())
    
    # ---------
    #  Landsat Zoomin
    # ---------

    lon = np.linspace(start=abox[0], stop=abox[2], num=landsat.shape[1])
    lat = np.linspace(start=abox[1], stop=abox[3], num=landsat.shape[0])
    lon, lat = np.meshgrid(lon, lat)
    
    ax5.set_title("(e) Zoomed Landsat " + ftype, fontsize=18)
    ax5.set_extent(area, crs=ccrs.PlateCarree())
    ax5.add_feature(cf.COASTLINE, linewidth=2.5)
    cm = ax5.pcolormesh(lon, lat, np.flipud(landsat), cmap='RdYlGn', transform=ccrs.PlateCarree(), vmax=1, vmin=-1, rasterized=True)
    gls = ax5.gridlines(draw_labels=False, crs=ccrs.PlateCarree(), linestyle='--', zorder=4)
    x = np.round(np.linspace(area[0], area[1], 3), 2)
    y = np.round(np.linspace(area[2], area[3], 3), 2)
    gls.xlocator = mticker.FixedLocator(x)
    gls.ylocator = mticker.FixedLocator(y)
    ax5.set_xticks(x)
    ax5.set_yticks(y)
    ax5.set_xlabel('Longitude', fontsize=16)
    ax5.set_ylabel('Latitude', fontsize=16)
    ax5.plot([area[1], area[1], area[0], area[0], area[1]], [area[2], area[3], area[3], area[2], area[2]],
         color='orange', linewidth=6,
         transform=ccrs.PlateCarree())
    
    # ---------
    #  SR Zoomin
    # ---------    
    ax6.set_title("(f) Zoomed Downscaled " + ftype, fontsize=18)
    ax6.set_extent(area, crs=ccrs.PlateCarree())
    ax6.add_feature(cf.COASTLINE, linewidth=2.5)
    cm = ax6.pcolormesh(lon, lat, np.flipud(sr), cmap='RdYlGn', transform=ccrs.PlateCarree(), vmax=1, vmin=-1, rasterized=True)
    gls = ax6.gridlines(draw_labels=False, crs=ccrs.PlateCarree(), linestyle='--', zorder=4)
    x = np.round(np.linspace(area[0], area[1], 3), 2)
    y = np.round(np.linspace(area[2], area[3], 3), 2)
    gls.xlocator = mticker.FixedLocator(x)
    gls.ylocator = mticker.FixedLocator(y)
    ax6.set_xticks(x)
    ax6.set_yticks(y)
    ax6.set_xlabel('Longitude', fontsize=16)
    ax6.set_ylabel('Latitude', fontsize=16)
    ax6.plot([area[1], area[1], area[0], area[0], area[1]], [area[2], area[3], area[3], area[2], area[2]],
         color='red', linewidth=6,
         transform=ccrs.PlateCarree())
    
    # cbaxes = fig.add_axes([0.92, 0.12, 0.01, 0.75])  # [left, bottom, width, height]
    # cb = fig.colorbar(cm, cax=cbaxes, location="bottom")
    # cb.set_label(ftype, fontsize=14)
    
    fig.tight_layout()
    
    p0 = ax3.get_position().get_points().flatten()
    p1 = ax6.get_position().get_points().flatten()
    ax_cbar = fig.add_axes([p1[2] + 0.02, p1[1], 0.01, p0[3] -  p1[1]])
    cb = plt.colorbar(cm, cax=ax_cbar)
    cb.set_label(ftype, fontsize=15)
    cb.ax.tick_params(labelsize=13)
    
    plt.savefig(workpath + '/Plots/VIs_6figs/'  + fdate + '.' + ftype + ".pdf", format='pdf',
            bbox_inches='tight', facecolor=(1, 1, 1, 0))
    plt.close()


def plot_test_example_HW(filedate):
    hr_height = 2000
    hr_width = 2656
    # load sr outputs
    filename = workpath + 'Results/Variables/Test_SR_HW/VI.' + filedate + '.HW.npy'
    sr = np.load(filename, allow_pickle=True)
    sr_ndvi = sr[0, :hr_height, :hr_width]
    sr_evi = sr[1, :hr_height, :hr_width]
    sr_evi2 = sr[2, :hr_height, :hr_width]

    # load interpolation outputs
    filename = workpath + 'Results/Variables/Test_Interpolation_HW/VI.' + filedate + '.HW.npy'
    intero = np.load(filename, allow_pickle=True)
    intero_ndvi = intero[0, :hr_height, :hr_width]
    intero_evi = intero[1, :hr_height, :hr_width]
    intero_evi2 = intero[2, :hr_height, :hr_width]

    # load landsat and viirs
    filename = workpath + 'ML_VI_Data_HW/Test/VI.' + filedate + '.HW.h5'
    file = h5py.File(filename, 'r')
    viirs = np.array(file['viirs'][:])
    landsat = np.array(file['landsat'][:])
    file.close()

    viirs_ndvi = viirs[0]
    viirs_evi = viirs[1]
    viirs_evi2 = viirs[2]

    landsat_ndvi = landsat[0]
    landsat_evi = landsat[1]
    landsat_evi2 = landsat[2]

    # load mask
    y_mask = np.load(workpath + 'Masks/Mask.30m.npy')
    y_mask[y_mask == 0 ] = np.nan
    x_mask = np.load(workpath + 'Masks/Mask.480m.npy')
    x_mask[x_mask == 0 ] = np.nan

    # apply mask
    sr_ndvi *= y_mask
    sr_evi *= y_mask
    sr_evi2 *= y_mask

    intero_ndvi *= y_mask
    intero_evi *= y_mask
    intero_evi2 *= y_mask

    landsat_ndvi *= y_mask
    landsat_evi *= y_mask
    landsat_evi2 *= y_mask

    viirs_ndvi *= x_mask
    viirs_evi *= x_mask
    viirs_evi2 *= x_mask


    sr_ndvi *= 1.2
    sr_evi *= 0.75
    sr_evi2 *= 1.2

    plot_function(viirs_ndvi, landsat_ndvi, sr_ndvi, intero_ndvi, ftype="NDVI", fdate = filedate)
    plot_function(viirs_evi, landsat_evi, sr_evi, intero_evi, ftype="EVI", fdate = filedate)
    plot_function(viirs_evi2, landsat_evi2, sr_evi2, intero_evi2, ftype="EVI2", fdate = filedate)
    
    
import os
filelist = os.listdir(workpath + 'Results/Variables/Test_SR_HW/')

# plot_test_example_HW(filelist[0][3:11])
plot_test_example_HW('2020.195')

# for filename in filelist:
#     filedate = filename[3:11]
#     print(filedate)
#     plot_test_example_HW(filedate)
