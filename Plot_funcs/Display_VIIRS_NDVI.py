import numpy as np
import matplotlib.pyplot as plt
import numpy as np


def plot_example(data, figurename):
    fig = plt.figure()

    im = plt.imshow(data, cmap='RdYlGn', vmax=1.5, vmin=-1.5)
    plt.title('VIIRS-NDVI')
    plt.colorbar(im, fraction=0.04, pad=0.025)

    # save figure
    plt.savefig('/net/airs1/storage/people/mgcy/Projects/VIIRS_Super_Resolution/VIIRS_NDVI_CO_Plots/' + figurename + '.png', format='png',
                bbox_inches='tight')

    plt.close(fig)


savepath = '/net/airs1/storage/people/mgcy/Projects/VIIRS_Super_Resolution/VIIRS_VI_CO/'

# CO
start_doy_dict = {'2018': '9',
                  '2019': '1',
                  '2020': '1',
                  '2021': '1',
                  '2022': '1',
                  '2023': '1', }


for year in range(2018, 2024):
    year = str(year)
    start_doy = start_doy_dict[year]
    for doy in range(int(start_doy), 366, 16):
        doy = str(doy).zfill(3)
        # print(year + ' ' + doy)
        try:
            # figurename = 'VIIRS.NDVI.' + year + '.' + str(doy)
            figurename = 'VIIRS.VNP13.VI.' + year + '.' + str(doy)
            ndvi = np.load(savepath + figurename + '.npy')[0]/10000.0
            print("Load data")
            plot_example(ndvi, figurename)
        except:
            print('Data issue @ ' +  doy)
