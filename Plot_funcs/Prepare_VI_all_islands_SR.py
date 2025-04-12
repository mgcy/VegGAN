import numpy as np
import cv2
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import cartopy.feature as cf
import gc
import matplotlib.ticker as mticker

workpath = '/net/airs1/storage/people/mgcy/Projects/VIIRS_Super_Resolution/'
product_index = 2


Island_abox = {'Maui': [-156.75, 20.45, -155.95, 21.05],
               'Oahu': [-158.4, 21.2, -157.6, 21.8],
               'Molokai': [-157.35, 20.7, -157.35 + 0.8, 20.7 + 0.6],
               'Kauai': [-159.9, 21.8, -159.1, 22.4],
               'Niihau': [-160.7, 21.6, -160.7 + 0.8, 21.6 + 0.6],
               'Big': [-156.2, 18.9, -154.8, 20.3]}

abox = [-160.3, 18.85, -154.7, 22.35]

target_nx = int((abox[2] - abox[0]) / 0.0003)
target_ny = int((abox[3] - abox[1]) / 0.0003)

# vi = np.zeros((target_ny, target_nx)).astype('float16')

lon = np.linspace(start=abox[0], stop=abox[2], num=target_nx).astype('float16')
lat = np.linspace(start=abox[3], stop=abox[1], num=target_ny).astype('float16')
# lonm, latm = np.meshgrid(lon, lat)
    

def plot_function(data):
    states_provinces = cf.NaturalEarthFeature(
    category='cultural',
    name='admin_1_states_provinces_lines',
    scale='50m',
    facecolor='none')

    fig = plt.figure(figsize=[10, 4])
    ax1 = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())

    lon = np.linspace(start=abox[0], stop=abox[2], num=data.shape[1])
    lat = np.linspace(start=abox[1], stop=abox[3], num=data.shape[0])
    lon, lat = np.meshgrid(lon, lat)

    ax1.set_title("(a) SR NDVI")

    ax1.add_feature(states_provinces, edgecolor='black', linewidth=2.5, zorder=3)
    ax1.add_feature(cf.LAND)
    ax1.add_feature(cf.OCEAN, zorder=3)
    ax1.add_feature(cf.COASTLINE, linewidth=2.5)
    ax1.add_feature(cf.BORDERS, linestyle=':')

    cm = ax1.pcolormesh(lon, lat, np.flipud(data), cmap='RdYlGn', transform=ccrs.PlateCarree(), vmax=1, vmin=-1, rasterized=True)

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
    cb = fig.colorbar(cm)
    cb.set_label('NDVI', fontsize=14)

    # plt.savefig(workpath + '/Plots/MVC/'  + fdate + '.' + ftype + ".png", format='png',
    #         bbox_inches='tight', facecolor=(1, 1, 1, 0))
    plt.savefig('tmp2.png')
    plt.close()




def fill_vi(tmp_sr_data, extra):
    vi = np.zeros((target_ny, target_nx)).astype('float16')
    i = 0
    for Island_name in ['Maui', 'Oahu', 'Molokai', 'Kauai', 'Niihau']:
    # for Island_name in ['Maui']:
        print(Island_name)
        limit = Island_abox[Island_name]

        # loc = np.where((lonm >= limit[0]) & (lonm <= limit[1]) & (
        #     latm >= limit[2]) & (latm <= limit[3]))
        # a = np.min(loc[0])
        # b = np.max(loc[0])
        # c = np.min(loc[1])
        # d = np.max(loc[1])
        # print(a,b,c,d)
        
        loc1 = np.where((lon >= limit[0]) & (lon <= limit[2]))
        loc2 = np.where((lat >= limit[1]) & (lat <= limit[3]))
        a = np.min(loc2[0])
        b = np.max(loc2[0])
        c = np.min(loc1[0])
        d = np.max(loc1[0])
        print(a,b,c,d)
        print('resize')
        vi[a:b, c:d] = cv2.resize(tmp_sr_data[i, product_index, :2000], (d-c, b-a), interpolation=cv2.INTER_CUBIC).astype('float16')
        i += 1
        
    limit = [-156.2, 18.9, -154.8, 20.3]
    loc1 = np.where((lon >= limit[0]) & (lon <= limit[2]))
    loc2 = np.where((lat >= limit[1]) & (lat <= limit[3]))
    a = np.min(loc2[0])
    b = np.max(loc2[0])
    c = np.min(loc1[0])
    d = np.max(loc1[0])
    print(a,b,c,d)
    print('resize')
    vi[a:b, c:d] = cv2.resize(extra, (d-c, b-a), interpolation=cv2.INTER_CUBIC).astype('float16')

        
    gc.collect()

    return vi


sr_path = '/net/airs1/storage/people/mgcy/Projects/VIIRS_Super_Resolution/Results/Variables/VI_Test_All_Islands/'
viirs_path = '/net/airs1/storage/people/mgcy/Projects/VIIRS_Super_Resolution/VIIRS_VI_Test_All_Islands/'

year = '2023'
doy = '193'

# load SR
sr_vi_path = sr_path + 'SR.VNP13.VI.Test.' + year + '.' + str(doy) + '.npy'
tmp_sr_data = np.load(sr_vi_path)


tmp_sr_data_ul = np.load(sr_vi_path)[5, product_index, :2000]
tmp_sr_data_ur = np.load(sr_vi_path)[6, product_index, :2000]
tmp_sr_data_ml = np.load(sr_vi_path)[7, product_index, :2000]
tmp_sr_data_mr = np.load(sr_vi_path)[8, product_index, :2000]
tmp_sr_data_bl = np.load(sr_vi_path)[9, product_index, :2000]
tmp_sr_data_br = np.load(sr_vi_path)[10, product_index, :2000]

sr_tmp1 = np.concatenate((tmp_sr_data_ul[:1664], tmp_sr_data_ml[320:1664], tmp_sr_data_bl[320:]), axis = 0)
sr_tmp2 = np.concatenate((tmp_sr_data_ur[:1664], tmp_sr_data_mr[320:1664], tmp_sr_data_br[320:]), axis = 0)
sr_tmp = np.concatenate((sr_tmp1[:, :2320], sr_tmp2[:, 320:]), axis = 1)

del sr_tmp1, sr_tmp2, tmp_sr_data_ul, tmp_sr_data_ur, tmp_sr_data_ml, tmp_sr_data_mr, tmp_sr_data_bl, tmp_sr_data_br

vi = fill_vi(tmp_sr_data, sr_tmp)

del tmp_sr_data, sr_tmp
gc.collect()
print('plot')
plt.imshow(vi)
plt.savefig('tmp.png')
np.save('tmp.npy', vi)
# plot_function(vi)