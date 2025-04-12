import numpy as np
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import cartopy.feature as cf
import gc
import matplotlib.ticker as mticker
import rasterio

workpath = '/net/airs1/storage/people/mgcy/Projects/VIIRS_Super_Resolution/'

file = rasterio.open(workpath + 'SR_VI_Results_HW/GeoTiff/VIIRS-Merged-2023-193-EVI2.tif')

data = file.read()[0]
# Get the bounding box in the format (left, bottom, right, top)
bounds = file.bounds

# Extract the latitude and longitude coordinates
min_lon, min_lat, max_lon, max_lat = bounds
print(min_lon, min_lat, max_lon, max_lat)

print(data.shape)

del file
# abox = [-160.3, 18.85, -154.7, 22.35]
# abox = [-160.70015060240962, 18.899853537862853, -154.8000646917568, 22.402259036144585]
abox = [min_lon, min_lat, max_lon, max_lat]

# plot_function(vi)

area1 = [-159.50, -159.42, 22.10, 22.16]
area2 = [-158.00,  -157.92, 21.50, 21.56]
area3 = [-156.95, -156.87, 21.08, 21.14]
area4 = [-155.58, -155.5, 19.96, 20.02]

# states_provinces = cf.NaturalEarthFeature(
# category='cultural',
# name='admin_1_states_provinces_lines',
# scale='50m',
# facecolor='none')

fig = plt.figure(figsize=[12,5])
ax1 = fig.add_subplot(1, 4, 1, projection=ccrs.PlateCarree())
ax2 = fig.add_subplot(1, 4, 2, projection=ccrs.PlateCarree())
ax3 = fig.add_subplot(1, 4, 3, projection=ccrs.PlateCarree())
ax4 = fig.add_subplot(1, 4, 4, projection=ccrs.PlateCarree())

lon = np.linspace(start=abox[0], stop=abox[2], num=data.shape[1])
lat = np.linspace(start=abox[1], stop=abox[3], num=data.shape[0])
lon, lat = np.meshgrid(lon, lat)

# ---------
#    1
# ---------
    
ax1.set_title("(b) Zoomed VIIRS EVI2 on Kauai")
cm = ax1.imshow(data, extent=(abox[0], abox[2], abox[1], abox[3]), cmap='RdYlGn', transform=ccrs.PlateCarree(), vmax=1, vmin=-1, rasterized=True)

gls = ax1.gridlines(draw_labels=False, crs=ccrs.PlateCarree(), linestyle='--', zorder=4)

x = np.round(np.linspace(area1[0], area1[1], 3), 2)
y = np.round(np.linspace(area1[2], area1[3], 3), 2)

gls.xlocator = mticker.FixedLocator(x)
gls.ylocator = mticker.FixedLocator(y)

ax1.set_xticks(x)
ax1.set_yticks(y)
ax1.set_xlim(area1[0], area1[1])
ax1.set_ylim(area1[2], area1[3])
ax1.ticklabel_format(useOffset=False)
ax1.set_xlabel('Longitude')
ax1.set_ylabel('Latitude')

# ---------
#    2
# ---------
    
ax2.set_title("(c) Zoomed VIIRS EVI2 on Oahu")
cm = ax2.imshow(data, extent=(abox[0], abox[2], abox[1], abox[3]), cmap='RdYlGn', transform=ccrs.PlateCarree(), vmax=1, vmin=-1, rasterized=True)

gls = ax2.gridlines(draw_labels=False, crs=ccrs.PlateCarree(), linestyle='--', zorder=4)

ax1.coastlines()

x = np.round(np.linspace(area2[0], area2[1], 3), 2)
y = np.round(np.linspace(area2[2], area2[3], 3), 2)

gls.xlocator = mticker.FixedLocator(x)
gls.ylocator = mticker.FixedLocator(y)

ax2.set_xticks(x)
ax2.set_yticks(y)
ax2.set_xlim(area2[0], area2[1])
ax2.set_ylim(area2[2], area2[3])

ax2.ticklabel_format(useOffset=False)

ax2.set_xlabel('Longitude')
ax2.set_ylabel('Latitude')

# ---------
#    3
# ---------
    
ax3.set_title("(d) Zoomed VIIRS EVI2 on Molokai")
cm = ax3.imshow(data, extent=(abox[0], abox[2], abox[1], abox[3]), cmap='RdYlGn', transform=ccrs.PlateCarree(), vmax=1, vmin=-1, rasterized=True)

gls = ax3.gridlines(draw_labels=False, crs=ccrs.PlateCarree(), linestyle='--', zorder=4)

x = np.round(np.linspace(area3[0], area3[1], 3), 2)
y = np.round(np.linspace(area3[2], area3[3], 3), 2)

gls.xlocator = mticker.FixedLocator(x)
gls.ylocator = mticker.FixedLocator(y)

ax3.set_xticks(x)
ax3.set_yticks(y)
ax3.set_xlim(area3[0], area3[1])
ax3.set_ylim(area3[2], area3[3])
ax3.ticklabel_format(useOffset=False)
ax3.set_xlabel('Longitude')
ax3.set_ylabel('Latitude')

# ---------
#    4
# ---------
    
ax4.set_title("(e) Zoomed VIIRS EVI2 on Big Island")

cm = ax4.imshow(data, extent=(abox[0], abox[2], abox[1], abox[3]), cmap='RdYlGn', transform=ccrs.PlateCarree(), vmax=1, vmin=-1, rasterized=True)

gls = ax4.gridlines(draw_labels=False, crs=ccrs.PlateCarree(), linestyle='--', zorder=4)

# ax4.coastlines()

x = np.round(np.linspace(area4[0], area4[1], 3), 2)
y = np.round(np.linspace(area4[2], area4[3], 3), 2)

gls.xlocator = mticker.FixedLocator(x)
gls.ylocator = mticker.FixedLocator(y)

ax4.set_xticks(x)
ax4.set_yticks(y)
ax4.set_xlim(area4[0], area4[1])
ax4.set_ylim(area4[2], area4[3])
ax4.ticklabel_format(useOffset=False)

ax4.set_xlabel('Longitude')
ax4.set_ylabel('Latitude')


ax1.plot([area1[1], area1[1], area1[0], area1[0], area1[1]], [area1[2], area1[3], area1[3], area1[2], area1[2]],
         color='blue', linewidth=6,
         transform=ccrs.PlateCarree())

ax2.plot([area2[1], area2[1], area2[0], area2[0], area2[1]], [area2[2], area2[3], area2[3], area2[2], area2[2]],
         color='cyan', linewidth=6,
         transform=ccrs.PlateCarree())

ax3.plot([area3[1], area3[1], area3[0], area3[0], area3[1]], [area3[2], area3[3], area3[3], area3[2], area3[2]],
         color='darkorange', linewidth=6,
         transform=ccrs.PlateCarree())

ax4.plot([area4[1], area4[1], area4[0], area4[0], area4[1]], [area4[2], area4[3], area4[3], area4[2], area4[2]],
         color='red', linewidth=6,
         transform=ccrs.PlateCarree())

fig.tight_layout(pad=0.1)

# p0 = ax3.get_position().get_points().flatten()
# p1 = ax4.get_position().get_points().flatten()
# ax_cbar = fig.add_axes([p0[0], 0.04, p1[2]-p0[0], 0.01])
# cb = plt.colorbar(cm, cax=ax_cbar, orientation='horizontal')
    
# p0 = ax2.get_position().get_points().flatten()
# p1 = ax4.get_position().get_points().flatten()
# ax_cbar = fig.add_axes([p1[2] + 0.04, p1[1], 0.01, p0[3] -  p1[1]])
# cb = plt.colorbar(cm, cax=ax_cbar)
# cb.set_label('EVI2', fontsize=13)
# cb.ax.tick_params(labelsize=13)
    
del data
gc.collect()
print('save')
# plt.savefig(workpath + '/Plots/MVC/'  + fdate + '.' + ftype + ".png", format='png',
#         bbox_inches='tight', facecolor=(1, 1, 1, 0))
plt.savefig(workpath + '/Plots/All_Islands_zoomin/VIIRS.EVI2.All.Islands.boxes.pdf', bbox_inches='tight', facecolor=(1, 1, 1, 0))
plt.close()
