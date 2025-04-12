import numpy as np
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import cartopy.feature as cf
import gc
import matplotlib.ticker as mticker
import rioxarray as rxr
import matplotlib.pyplot as plt
import numpy as np
import cv2
import rasterio

workpath = '/net/airs1/storage/people/mgcy/Projects/VIIRS_Super_Resolution/'

file = rasterio.open(workpath + 'SR_VI_Results_HW/GeoTiff/SR-Merged-2023-193-EVI2.tif')

data = file.read()[0]
# Get the bounding box in the format (left, bottom, right, top)
bounds = file.bounds

# Extract the latitude and longitude coordinates
min_lon, min_lat, max_lon, max_lat = bounds
print(min_lon, min_lat, max_lon, max_lat)

print(data.shape)

data *=2
# abox = [-160.3, 18.85, -154.7, 22.35]
# abox = [-160.70015060240962, 18.899853537862853, -154.8000646917568, 22.402259036144585]
abox = [min_lon, min_lat, max_lon, max_lat]

states_provinces = cf.NaturalEarthFeature(
category='cultural',
name='admin_1_states_provinces_lines',
scale='50m',
facecolor='none')

fig = plt.figure(figsize=[16, 8])
ax1 = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
ax1.set_extent([-160.3, -154.7, 18.85, 22.35], crs=ccrs.PlateCarree())
lon = np.linspace(start=abox[0], stop=abox[2], num=data.shape[1])
lat = np.linspace(start=abox[1], stop=abox[3], num=data.shape[0])
lon, lat = np.meshgrid(lon, lat)

ax1.set_title("(a) Downscaled VIIRS EVI2")

ax1.add_feature(states_provinces, edgecolor='black', linewidth=2.5, zorder=3)
ax1.add_feature(cf.LAND)
# ax1.add_feature(cf.OCEAN, zorder=3)
ax1.add_feature(cf.COASTLINE, linewidth=2.5)
ax1.add_feature(cf.BORDERS, linestyle=':')
print('save')
cm = ax1.imshow(data, extent=(abox[0], abox[2], abox[1], abox[3]), cmap='RdYlGn', transform=ccrs.PlateCarree(), vmax=1, vmin=-1, rasterized=True)
print('save111')

gls = ax1.gridlines(draw_labels=False, crs=ccrs.PlateCarree(), linestyle='--', zorder=4, color='black')

ax1.coastlines()

cbox = [-160.3, 18.85, -154.7, 22.35]

x = np.round(np.linspace(cbox[0], cbox[2], 5), 2)
y = np.round(np.linspace(cbox[1], cbox[3], 4), 2)

gls.xlocator = mticker.FixedLocator(x)
gls.ylocator = mticker.FixedLocator(y)

area1 = [-159.5, -159.42, 22.1, 22.16]
area2 = [-158,  -157.92, 21.5, 21.56]
area3 = [-156.95, -156.87, 21.08, 21.14]
area4 = [-155.58, -155.5, 19.96, 20.02]

ax1.plot([area1[1], area1[1], area1[0], area1[0], area1[1]], [area1[2], area1[3], area1[3], area1[2], area1[2]],
         color='blue', linewidth=2,
         transform=ccrs.PlateCarree())

ax1.plot([area2[1], area2[1], area2[0], area2[0], area2[1]], [area2[2], area2[3], area2[3], area2[2], area2[2]],
         color='cyan', linewidth=2,
         transform=ccrs.PlateCarree())

ax1.plot([area3[1], area3[1], area3[0], area3[0], area3[1]], [area3[2], area3[3], area3[3], area3[2], area3[2]],
         color='darkorange', linewidth=2,
         transform=ccrs.PlateCarree())

ax1.plot([area4[1], area4[1], area4[0], area4[0], area4[1]], [area4[2], area4[3], area4[3], area4[2], area4[2]],
         color='red', linewidth=2,
         transform=ccrs.PlateCarree())


ax1.set_xticks(x)
ax1.set_yticks(y)
ax1.set_xlabel('Longitude')
ax1.set_ylabel('Latitude')
cb = fig.colorbar(cm, aspect=35, pad=0.01)
cb.set_label('EVI2', fontsize=14)

del data
gc.collect()
print('save')
# plt.savefig(workpath + '/Plots/MVC/'  + fdate + '.' + ftype + ".png", format='png',
#         bbox_inches='tight', facecolor=(1, 1, 1, 0))
plt.savefig(workpath + '/Plots/All_Islands_zoomin/SR.EVI2.All.Islands.Geotif.pdf', bbox_inches='tight', facecolor=(1, 1, 1, 0))
plt.close()
