import os
import tarfile

for year in range(2023,2024):
    year = str(year)
    
    # datapath = '/net/airs1/storage/people/mgcy/Data/Landsat_CO_raw/' + year + '/'
    datapath = '/net/airs1/storage/people/mgcy/Data/Landsat_HW_raw/' + year + '/'
    filelist = os.listdir(datapath)
    filelist.sort()
    
    # savepath = '/net/airs1/storage/people/mgcy/Projects/VIIRS_Super_Resolution/Landsat_CO_untar/' + year + '/'
    savepath = '/net/airs1/storage/people/mgcy/Projects/VIIRS_Super_Resolution/Landsat_HW_untar/' + year + '/'
    
    for filename in filelist:
        if 'LC08' in filename:
            if not os.path.exists(savepath + filename[:-4]):
                os.makedirs(savepath + filename[:-4])

            tar = tarfile.open(datapath + filename)
            tar.extractall(savepath + filename[:-4])
            tar.close()
