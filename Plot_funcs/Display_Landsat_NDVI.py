import numpy as np
import matplotlib.pyplot as plt
import numpy as np


def plot_example(data, figurename):
    fig = plt.figure()

    im = plt.imshow(data, cmap='RdYlGn')
    plt.title(figurename)
    plt.colorbar(im, fraction=0.04, pad=0.025)

    # save figure
    plt.savefig('/net/airs1/storage/people/mgcy/Projects/VIIRS_Super_Resolution/Landsat_VI_Plots/' + figurename + '.png', format='png',
                bbox_inches='tight')

    plt.close(fig)


savepath = '/net/airs1/storage/people/mgcy/Projects/VIIRS_Super_Resolution/Landsat_NDVI/'

start_doy_dict = {'2015': '10',
                  '2016': '13',
                  '2017': '15',
                  '2018': '2',
                  '2019': '5',
                  '2020': '8',
                  '2021': '10',
                  '2022': '13', }


for year in range(2015, 2023):
    year = str(year)
    start_doy = start_doy_dict[year]
    for doy in range(int(start_doy), 366, 16):
        doy = str(doy).zfill(3)
        # print(year + ' ' + doy)
        try:
            figurename = 'Landsat.NDVI.' + year + '.' + str(doy)
            ndvi = np.load(savepath + figurename + '.npy')
            plot_example(ndvi, figurename)
        except:
            print('Data issue @ ' +  doy)
