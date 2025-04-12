import os
import logging

logging.basicConfig(filename="Download.VIIRS.log", level=logging.INFO,
                    format='%(asctime)s %(message)s',
                    filemode='w')


# check https://earthexplorer.usgs.gov/ and 
# FIRMS orbit for these dates
start_doy_dict = {'2015':'10', 
                  '2016':'13',
                  '2017':'15',
                  '2018':'2',
                  '2019':'5',
                  '2020':'8',
                  '2021':'10',
                  '2022':'13',}


for year in range(2022,2023):
    year = str(year)
    start_doy = start_doy_dict[year]
    for i in range(int(start_doy), 366, 16):
        doy = str(i).zfill(3)
        logging.info(year + ' ' +  doy)

        # download VNP02
        cmd_tmp1 = 'wget -e robots=off -m -np -R .html,.tmp -nH -A "VNP02IMG.*.2000.002*.nc" --cut-dirs=3 "https://ladsweb.modaps.eosdis.nasa.gov/archive/allData/5200/VNP02IMG/' + year + '/' + doy + '/" --header "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJvcmlnaW4iOiJFYXJ0aGRhdGEgTG9naW4iLCJzaWciOiJlZGxqd3RwdWJrZXlfb3BzIiwiYWxnIjoiUlMyNTYifQ.eyJ0eXBlIjoiVXNlciIsInVpZCI6Im1nY3kiLCJleHAiOjE3Mjk2MjY5MDMsImlhdCI6MTcyNDQ0MjkwMywiaXNzIjoiaHR0cHM6Ly91cnMuZWFydGhkYXRhLm5hc2EuZ292In0.gWyzKTnzef1M1gvXGrJWtzE4R9NUb7d_t0dEetnJWh_Ad2eFNhyghmAdk8muZB3lWb2UjYmbXGBMzYyRGCjUQRm2LjGZliFOxNrqPZDf5QqJjVjAcUU7WyPUoAjsFmXkyLWKw3jCYW8QZAomAUd--k7OySUzK8uAmBJu8F37oXXNHdTdsYTbMA6XiopmslzjET3-jAc7i6vHf5jFI-rkZJ9TLfeRWy1nuJDW4HgUAnF3-jHwVic-iUoadLqZhScOcDSp0Eiu69geBfZ0fsvLCqDu0yKAlaru9krwIJjTSXvKYg7xKFL6VkOG1KHYKf_dVJK2iK_pTp1rAAeoKFQ8xA" -P /net/airs1/storage/people/projects/'
        os.system(cmd_tmp1)
        
        # download VNP03
        cmd_tmp2 = 'wget -e robots=off -m -np -R .html,.tmp -nH -A "VNP03IMG.*.2000.002*.nc" --cut-dirs=3 "https://ladsweb.modaps.eosdis.nasa.gov/archive/allData/5200/VNP03IMG/' + year + '/' + doy + '/" --header "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJvcmlnaW4iOiJFYXJ0aGRhdGEgTG9naW4iLCJzaWciOiJlZGxqd3RwdWJrZXlfb3BzIiwiYWxnIjoiUlMyNTYifQ.eyJ0eXBlIjoiVXNlciIsInVpZCI6Im1nY3kiLCJleHAiOjE3Mjk2MjY5MDMsImlhdCI6MTcyNDQ0MjkwMywiaXNzIjoiaHR0cHM6Ly91cnMuZWFydGhkYXRhLm5hc2EuZ292In0.gWyzKTnzef1M1gvXGrJWtzE4R9NUb7d_t0dEetnJWh_Ad2eFNhyghmAdk8muZB3lWb2UjYmbXGBMzYyRGCjUQRm2LjGZliFOxNrqPZDf5QqJjVjAcUU7WyPUoAjsFmXkyLWKw3jCYW8QZAomAUd--k7OySUzK8uAmBJu8F37oXXNHdTdsYTbMA6XiopmslzjET3-jAc7i6vHf5jFI-rkZJ9TLfeRWy1nuJDW4HgUAnF3-jHwVic-iUoadLqZhScOcDSp0Eiu69geBfZ0fsvLCqDu0yKAlaru9krwIJjTSXvKYg7xKFL6VkOG1KHYKf_dVJK2iK_pTp1rAAeoKFQ8xA" -P /net/airs1/storage/people/projects/'
        os.system(cmd_tmp2)
