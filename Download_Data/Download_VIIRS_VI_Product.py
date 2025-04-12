import os
import logging

logging.basicConfig(filename="Download.VIIRS.VI.log", level=logging.INFO,
                    format='%(asctime)s %(message)s',
                    filemode='w')

# TOKEN = 'eyJ0eXAiOiJKV1QiLCJvcmlnaW4iOiJFYXJ0aGRhdGEgTG9naW4iLCJzaWciOiJlZGxqd3RwdWJrZXlfb3BzIiwiYWxnIjoiUlMyNTYifQ.eyJ0eXBlIjoiVXNlciIsInVpZCI6Imx1a2V0YXVsYmVlIiwiZXhwIjoxNzMwNTgwOTczLCJpYXQiOjE3MjUzOTY5NzMsImlzcyI6Imh0dHBzOi8vdXJzLmVhcnRoZGF0YS5uYXNhLmdvdiJ9.usXlqz3NdNiKY2MbrxD94y5NrHSuzloS8rwheD-xZBwmDjUWUW4ZOpiEPPN8dMVuoykpPDGmmalPgBQhADiwnQQTdNla6kpFxumEpIQ1fBr2LkuLOsvDH__s1_lfaZrwwURkg82tR3k-2heR2UHAoOtasqBK4nCSZmSgUNpjWrsc1bQRDWTOFmK1ohpcpSJjucORqN0OvJ1SV8YZpHj38pcNFlVkCp1uc15fuGFlYQJcLiHotR2J_9hlcHT1OtxRxpc4gM6eV-wR4hYG5P23tD58SC8whgiD_f9Ut95bnYS-I9_ySvQSDj0K1usFVXGIf7wT5tJjWY8-0_fRA0xCgw'
# check https://earthexplorer.usgs.gov/ and 
# FIRMS orbit for these dates
start_doy_dict = {
                  '2013':'1',
                  '2014':'1',
                  '2015':'1',
                  '2016':'1',
                  '2017':'1',
                  '2018':'1',
                  '2019':'1',
                  '2020':'1',
                  '2021':'1',
                  '2022':'1',
                  '2023':'1',}


for year in range(2015,2018):
    year = str(year)
    start_doy = start_doy_dict[year]
    for i in range(int(start_doy), 366, 8):
        doy = str(i).zfill(3)
        logging.info(year + ' ' +  doy)
        try:
            # download VNP13 h03v06
            # CO: v09h04
            # cmd_tmp1 = 'wget -e robots=off -m -np -R .html,.tmp -nH -A "VNP13A1.*.h03v07.002.*.h5" --cut-dirs=3 "https://ladsweb.modaps.eosdis.nasa.gov/archive/allData/5200/VNP13A1/' + year + '/' + doy + '/" --header "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbF9hZGRyZXNzIjoieWlmYW55YW5nMTFAZ21haWwuY29tIiwiaXNzIjoiQVBTIE9BdXRoMiBBdXRoZW50aWNhdG9yIiwiaWF0IjoxNzA0NzgyNTMzLCJuYmYiOjE3MDQ3ODI1MzMsImV4cCI6MTg2MjQ2MjUzMywidWlkIjoibWdjeSIsInRva2VuQ3JlYXRvciI6Im1nY3kifQ.9RpG-VvNAt_wfTw60vT4ziDrY1Ay5VSU2hFESHJzAis" -P /net/airs1/storage/people/mgcy/Data/VIIRS_VNP13A1_HW_plus/'
            cmd_tmp1 = 'wget -e robots=off -m -np -R .html,.tmp -nH -A "VNP13A1.*.h03v06.002.*.h5" --cut-dirs=3 "https://ladsweb.modaps.eosdis.nasa.gov/archive/allData/5200/VNP13A1/' + year + '/' + doy + '/" --header "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJvcmlnaW4iOiJFYXJ0aGRhdGEgTG9naW4iLCJzaWciOiJlZGxqd3RwdWJrZXlfb3BzIiwiYWxnIjoiUlMyNTYifQ.eyJ0eXBlIjoiVXNlciIsInVpZCI6Im1nY3kiLCJleHAiOjE3Mjk2MjY5MDMsImlhdCI6MTcyNDQ0MjkwMywiaXNzIjoiaHR0cHM6Ly91cnMuZWFydGhkYXRhLm5hc2EuZ292In0.gWyzKTnzef1M1gvXGrJWtzE4R9NUb7d_t0dEetnJWh_Ad2eFNhyghmAdk8muZB3lWb2UjYmbXGBMzYyRGCjUQRm2LjGZliFOxNrqPZDf5QqJjVjAcUU7WyPUoAjsFmXkyLWKw3jCYW8QZAomAUd--k7OySUzK8uAmBJu8F37oXXNHdTdsYTbMA6XiopmslzjET3-jAc7i6vHf5jFI-rkZJ9TLfeRWy1nuJDW4HgUAnF3-jHwVic-iUoadLqZhScOcDSp0Eiu69geBfZ0fsvLCqDu0yKAlaru9krwIJjTSXvKYg7xKFL6VkOG1KHYKf_dVJK2iK_pTp1rAAeoKFQ8xA" -P /net/airs1/storage/people/mgcy/Data/VIIRS_VNP13A1_HW/'
            os.system(cmd_tmp1)
        except:
            logging.info('Issue @ ' + year + ' ' +  doy )

# Download for a single day

# year = '2023'
# for doy in [353,361]:
#     doy = str(doy).zfill(3)
#     logging.info(year + ' ' +  doy)
#     try:
#         # download VNP13 
#         # HW: h03v06
#         # CO: v09h04
#         # cmd_tmp1 = 'wget -e robots=off -m -np -R .html,.tmp -nH -A "VNP13A1.*.h03v07.002.*.h5" --cut-dirs=3 "https://ladsweb.modaps.eosdis.nasa.gov/archive/allData/5200/VNP13A1/' + year + '/' + doy + '/" --header "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbF9hZGRyZXNzIjoieWlmYW55YW5nMTFAZ21haWwuY29tIiwiaXNzIjoiQVBTIE9BdXRoMiBBdXRoZW50aWNhdG9yIiwiaWF0IjoxNzA0NzgyNTMzLCJuYmYiOjE3MDQ3ODI1MzMsImV4cCI6MTg2MjQ2MjUzMywidWlkIjoibWdjeSIsInRva2VuQ3JlYXRvciI6Im1nY3kifQ.9RpG-VvNAt_wfTw60vT4ziDrY1Ay5VSU2hFESHJzAis" -P /net/airs1/storage/people/mgcy/Data/VIIRS_VNP13A1_HW_plus/'
#         cmd_tmp1 = 'wget -e robots=off -m -np -R .html,.tmp -nH -A "VNP13A1.*.h03v06.002.*.h5" --cut-dirs=3 "https://ladsweb.modaps.eosdis.nasa.gov/archive/allData/5200/VNP13A1/' + year + '/' + doy + '//" --header "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJvcmlnaW4iOiJFYXJ0aGRhdGEgTG9naW4iLCJzaWciOiJlZGxqd3RwdWJrZXlfb3BzIiwiYWxnIjoiUlMyNTYifQ.eyJ0eXBlIjoiVXNlciIsInVpZCI6Im1nY3kiLCJleHAiOjE3Mjk2MjY5MDMsImlhdCI6MTcyNDQ0MjkwMywiaXNzIjoiaHR0cHM6Ly91cnMuZWFydGhkYXRhLm5hc2EuZ292In0.gWyzKTnzef1M1gvXGrJWtzE4R9NUb7d_t0dEetnJWh_Ad2eFNhyghmAdk8muZB3lWb2UjYmbXGBMzYyRGCjUQRm2LjGZliFOxNrqPZDf5QqJjVjAcUU7WyPUoAjsFmXkyLWKw3jCYW8QZAomAUd--k7OySUzK8uAmBJu8F37oXXNHdTdsYTbMA6XiopmslzjET3-jAc7i6vHf5jFI-rkZJ9TLfeRWy1nuJDW4HgUAnF3-jHwVic-iUoadLqZhScOcDSp0Eiu69geBfZ0fsvLCqDu0yKAlaru9krwIJjTSXvKYg7xKFL6VkOG1KHYKf_dVJK2iK_pTp1rAAeoKFQ8xA" -P /net/airs1/storage/people/mgcy/Data/VIIRS_VNP13A1_HW/'
#         os.system(cmd_tmp1)
#     except:
#         logging.info('Issue @ ' + year + ' ' +  doy )