# This is module 4 of 6
# This module calls the Companies document API, using metadata gathered from their main API (module 2)
# Created by Giselle Cory, 2018

# # # # # #
# # # # # #
# # # # # #
# Module 4: Documenet API call
# # # # # #
# # # # # #
# # # # # #

import pandas as pd
import numpy as np
import os.path
import requests
from pprint import pprint as print
import time
import datetime
import sys
import local_filepaths as fp

# # # # # #
# Create log file
# # # # # #

# Create log_filename CSV if it doesn't exist
if not os.path.isfile(fp.log_filepath/fp.log_filename):
    with open(fp.log_filepath/fp.log_filename, 'w'):
        pass

# # # # # #
# Read in data
# # # # # #

# Read in metadata master CSV
metadata_master = pd.read_csv(fp.meta_master, dtype={'co_numb': object, 'category': object, 'url': object, 'date': object, 'description': object, 'type': object, 'url': object, 'count_items': np.int64, 'year': np.int64, 'downloaded':np.int64, 'page_count':np.int64}, low_memory=False)

# Create a working version to ensure master is not unintentionally overwritten
meta_working = metadata_master.copy()
# Keep selected rows only - items not yet downloaded
meta_working = meta_working.loc[(meta_working['downloaded'] == 0)]

# Sort values
meta_working.sort_values(by=['co_numb'], inplace=True)
meta_working = meta_working.reset_index(drop=True)


def ErrorLog(e,j):
    print("ERROR: " + str(e))
    log_list = []
    log_dict = {}
    log_dict['api_type'] = "pdf"
    log_dict['_error_message'] = str(e)
    log_dict['_url'] = meta_working.at[j,'co_numb']
    log_dict['_time'] = str(datetime.datetime.now())
    log_list.append(log_dict)
    log_df = pd.DataFrame(log_list)
    log_df.to_csv(fp.log_filepath/fp.log_filename, index=False, mode='a')

# # # # # #
# Set up document API call
# # # # # #

# Globals
key = ENTER-API-KEY-HERE
gvDocApi = "http://document-api.companieshouse.gov.uk/document/"
rate_limit = 600

# Set header
doc_headers = {'Authorization': key, 'Accept': 'application/pdf'}

instance = 1

# Set a safeguard to ensure programme terminates
while instance < 7000 :

    # If this is not the first instance, calculate time needed for pause so that rate limit is not exeeded
    if instance != 1:
        sleep_duration = max(0, 301 - instance_duration)
        print("Sleeping zZzZ for " + str(round(sleep_duration,0)) + " seconds" )
        time.sleep(sleep_duration)

    # Begin new instance
    start_time = time.time()

    print("Instance: " + str(instance) + ". Run: " + str(rate_limit*(instance-1)) + " to " +  str(rate_limit*instance))

    # This instance will loop over conumpany numbers i to i + 600
    for j in range(rate_limit*(instance-1),rate_limit*instance):
        print("Request number " + str(j))
        print("Requesting PDF for " + str(meta_working.at[j,'co_numb']))

        # Create query URL
        request_url = gvDocApi + str(meta_working.at[j,'url']) + "/content"
        print(request_url)

        # # # # # #
        # Call API
        # # # # # #

        try:
            res = requests.get(request_url,headers=doc_headers)
        except requests.exceptions.ConnectionError as e:
            ErrorLog(e,j)
            continue

        try:
            res.raise_for_status()
        except requests.exceptions.RequestException as e:
            ErrorLog(e,j)
            continue

        # # # # # #
        # Save PDF locally
        # # # # # #

        pdf_name = str(meta_working.at[j,'co_numb']) + "_" + meta_working.at[j,'category'] + "_" + str(meta_working.at[j,'date']) + ".pdf"

        _dir_name = pdf_name[0:3]
        _destination_dir = str(fp.pdf_route_dir) +str(_dir_name)

        # Populate PDF
        with open(str(_destination_dir) +"/" + pdf_name,'wb') as f:
            f.write(res.content)

        # # # # # #
        # Update downloaded marker
        # # # # # #

        metadata_master["downloaded"][metadata_master['url'].str.match(meta_working.at[j,'url'])] = 1
        print(metadata_master.groupby(['downloaded']).size())

    # # # # # #
    # Save to file
    # # # # # #

    metadata_master.to_csv(fp.meta_master, index=False)
    print("Updated metadata_master CSV")

    # # # # # #
    # Note timing
    # # # # # #

    instance += 1
    end_time = time.time()
    instance_duration = end_time - start_time
    print("Instance duration is " + str(round(instance_duration,0)))

print("API calls finished")
