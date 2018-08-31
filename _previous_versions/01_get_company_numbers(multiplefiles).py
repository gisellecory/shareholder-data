# python3 A_setup/01_get_company_numbers.py

# # # # # #
# Get company numbers
# # # # # #

import warnings
warnings.filterwarnings("ignore")
import pandas as pd
from datetime import datetime

import sys
route_dir = "/Users/gisellecory/git/repo_shareholder_data"
sys.path.insert(0, route_dir)
import local

# For timing
startTime = datetime.now()

# co_numbs_file = "/Users/gisellecory/Documents/dissertation_store/01_input_CH_data/co_numbs_rebuild_v2.csv"

co_numbs_file = local.co_numbs_fp/local.co_numbs_all_fn

# Make sure that output CSV is empty to start with
f = open(co_numbs_file, "w+") # opening the file with w+ mode truncates the file
f.close()

# Open CH company numbers data
for i in range(0,5):
    print("Found: " + str(local.ch_data_src_list[i]))
    temp_data = pd.read_csv(local.co_numbs_fp/local.ch_data_src_list[i], low_memory=False)
    # Keep company numbers series only
    temp_data = temp_data[[' CompanyNumber']]

    # Rename series and save to CSV (for use in merge later on)
    temp_data = temp_data.rename(columns={' CompanyNumber': 'co_numb'})
    temp_data.to_csv(co_numbs_file, mode="a", index=False)

# Drop duplicates
print(len(temp_data))
temp_data.drop_duplicates(subset="co_numb",inplace=True)
print(temp_data.dtypes) # object
print(len(temp_data))

print("Saved: " + str(co_numbs_file))
# Note timing
print(datetime.now() - startTime)
