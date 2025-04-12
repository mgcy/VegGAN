from landsatxplore.api import API
from landsatxplore.earthexplorer import EarthExplorer
import json
import logging

logging.basicConfig(filename="Download.Landsat.log", level=logging.INFO,
                    format='%(asctime)s %(message)s',
                    filemode='w')

# Initialize a new API instance and get an access key
api = API('mgcy', 'gn@nY3H-+8?nTtG')

# Rocky MTN, CO: path=34,row=32
# Maui ISLD, HW, path=63,row=46
path_num = 63
row_num = 46

print(path_num, row_num)
fail_list = []

# Landsat 8 was launched on 11 February 2013
# We are using 2018 to 2022
for year in range(2014, 2015):
    year = str(year)
    logging.info('year %s', year)
    
    try:

        scenes = api.search(
            dataset='landsat_ot_c2_l1',
            wrs_path=path_num,
            wrs_row=row_num,
            start_date=year + '-01-01',
            end_date=year + '-12-31',
        )

        logging.info(f"{len(scenes)} scenes found.")

        # download using identifier id
        ee = EarthExplorer('mgcy', 'gn@nY3H-+8?nTtG')
        for i in range(len(scenes)):
            id = scenes[i]['display_id']
            logging.info(id)
            try: 
                ee.download(
                    id, output_dir='/net/airs1/storage/people/mgcy/Data/Landsat_HW_raw/'+year+'/')
            except:
                fail_list.append(id)
                logging.info('Downloading Failed @ %s: ', id)
    except:
        logging.info('Downloading year failed @: %s', year)
with open("Fail_List.json", 'w') as f:
    # indent=2 is not needed but makes the file human-readable 
    # if the data is nested
    json.dump(fail_list, f, indent=2) 