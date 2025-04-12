import h5py
import os
import numpy as np
import matplotlib.pyplot as plt
import cv2
import shutil


workpath = '/net/airs1/storage/people/mgcy/Projects/VIIRS_Super_Resolution/'

test_filelist = os.listdir(workpath + 'ML_VI_MVC_Data_HW/Test/')
test_filelist.sort()

# train_filelist = os.listdir(workpath + 'ML_VI_Data_HW/Train/')
# train_filelist.sort()

corr_thresold = 0.8

# for train_file in train_filelist:
# # for train_file in train_filelist[0:3]:
#     file = h5py.File(workpath + 'ML_VI_Data_HW/Train/' + train_file, 'r')
#     x = np.array(file['viirs'][:]) / 10000.0
#     y = np.array(file['landsat'][:])
#     file.close()

#     x[x>=1.1] = 1.1
#     x[x<=-1.1] = -1.1
#     x[x==-1.5] = 0

#     y[y>=1.1] = 1.1
#     y[y<=-1.1] = -1.1
#     y = np.where(np.isnan(y), 0, y)

#     # apply masks
#     x_mask = np.load(workpath + 'Code/Make_Mask/VIIRS_Mask_500m.npy')
#     y_mask = np.load(workpath + 'Code/Make_Mask/Landsat_Mask_500m.npy')

#     x[0] = x[0] * x_mask
#     x[1] = x[1] * x_mask
#     x[2] = x[2] * x_mask

#     y[0] = y[0] * y_mask
#     y[1] = y[1] * y_mask
#     y[2] = y[2] * y_mask

#     print(x.max(), x.min())
#     print(y.max(), y.min())

#     # flatten and calculate correlation coefficient
#     y_tmp = cv2.resize(y[0], (x.shape[2], x.shape[1]))
#     corr = np.corrcoef(x[0].flatten(), y_tmp.flatten())
#     # print(corr)
#     if corr[0, 1] > corr_thresold:
#         file = h5py.File(workpath + 'ML_VI_Data_HW/Train_Corr_Filter/' + train_file, 'w')
#         file.create_dataset('viirs', data = x)
#         file.create_dataset('landsat', data = y)
#         file.close()

for test_file in test_filelist:

    file = h5py.File(workpath + 'ML_VI_MVC_Data_HW/Test/' + test_file, 'r')
    x = np.array(file['viirs'][:]) 
    y = np.array(file['landsat'][:])
    file.close()

    # print(np.where(np.isnan(y)))
    y = np.where(np.isnan(y), 0, y)

    if x.max() > 1:
        print('x max: ', test_file)
        
    if y.max() > 1:
        print('y max: ', test_file)
        
    if x.max() < -1:
        print('x min: ', test_file)
        
    if x.max() < -1:
        print('y min: ', test_file)

    # flatten and calculate correlation coefficient
    y_tmp = cv2.resize(y[0], (x.shape[2], x.shape[1]))
    corr = np.corrcoef(x[0].flatten(), y_tmp.flatten())
    

    if corr[0, 1] > corr_thresold:
        file = h5py.File(workpath + 'ML_VI_MVC_Data_HW/Corr_Filter_Test/' + test_file, 'w')
        file.create_dataset('viirs', data = x)
        file.create_dataset('landsat', data = y)
        file.close()
    else:
        print(test_file, corr[0, 1])


'''
CC record:

VI.2019.016.HW.h5 0.7528973094684461
VI.2019.048.HW.h5 0.7647096719615664
VI.2019.064.HW.h5 0.7978480854416647
VI.2019.128.HW.h5 0.7404601617708201
VI.2019.144.HW.h5 0.7945448055089065
VI.2019.176.HW.h5 0.7958231691293252
VI.2019.336.HW.h5 0.7040105549674495
VI.2019.352.HW.h5 0.7367246567215205
VI.2020.003.HW.h5 0.6780800965421596
VI.2020.083.HW.h5 0.7795882901808201
VI.2020.099.HW.h5 0.7799654495455067
VI.2020.115.HW.h5 0.7629091196232994
VI.2020.131.HW.h5 0.7734484628309903
VI.2020.275.HW.h5 0.7938894631347442
VI.2020.291.HW.h5 0.7318467566081501
VI.2020.323.HW.h5 0.6419680353920513
VI.2020.339.HW.h5 0.738127281988532
VI.2020.355.HW.h5 0.734889802565666
VI.2021.005.HW.h5 0.7583511696278403
VI.2021.069.HW.h5 0.7797786559961865
VI.2021.117.HW.h5 0.7148718123522046
VI.2021.133.HW.h5 0.7762082789548725
VI.2021.197.HW.h5 0.7694532576874192
VI.2022.104.HW.h5 0.7439947321352404
VI.2022.120.HW.h5 0.7085741517629816
VI.2022.136.HW.h5 0.7305040417617893
VI.2022.184.HW.h5 0.7602860005547067
VI.2022.200.HW.h5 0.7174014487220726
VI.2022.248.HW.h5 0.7869238589098895
VI.2023.043.HW.h5 0.675477608541116
VI.2023.059.HW.h5 0.7153473273522071
VI.2023.155.HW.h5 0.7879493382604109
VI.2023.171.HW.h5 0.7955497492878155
VI.2023.187.HW.h5 0.7755144150507276
VI.2023.203.HW.h5 0.789095617879461
VI.2023.283.HW.h5 0.7816439542965945
VI.2023.331.HW.h5 0.7920901067581345
VI.2023.363.HW.h5 0.6101918402997085





'''