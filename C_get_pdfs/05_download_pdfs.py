# python3 02_get_pdfs/05_download_pdfs.py

# # # # # #
#  Main API call
# # # # # #

import warnings
warnings.filterwarnings("ignore")
import pandas as pd
import os.path
import requests
from pprint import pprint as print
import time
import datetime

import sys
route_dir = "/Users/gisellecory/git/repo_shareholder_data"
sys.path.insert(0, route_dir)
import local

destination_route_directory = local.filepath_pdf_directory

# Create log_filename CSV if it doesn't exist
if os.path.isfile(local.log_filepath/local.log_filename) == False:
    with open(local.log_filepath/local.log_filename, 'w'):
        pass

metadata_master = pd.read_csv(local.meta_master, low_memory=False)
metadata_master = metadata_master[metadata_master['doc_url'] != "none found/content"]

meta_working = metadata_master.copy()
# Selected rows only - items not yet downloaded
meta_working = meta_working.loc[(meta_working['downloaded'] == 0)]
# df.loc[(df['column_name'] == some_value)

# Selected columns only
# metadata_master = metadata_master[['category', 'co_numb', 'doc_url', 'date','downloaded']]
meta_working.sort_values(by=['co_numb'], inplace=True)
meta_working = meta_working.reset_index(drop=True)

# (3) Send updated URL list to API

# Globals
key = 'Basic a0k5MUxvNnlkbTBmdERneURBWXI1X0FHN002bkw5eHBzb1VLYXJkeQ=='

# Set header
doc_headers = {'Authorization': key, 'Accept': 'application/pdf'}

instance = 1
rate_limit = 600

while instance < 7000 :
    # downloaded_urls_list = []
    if instance != 1:
        sleep_duration = max(0, 301 - instance_duration) # 301 instead of 300 just in case, and max to deal with negative times
        # Take into account API rate limiting - wait 5 mins
        print("Sleeping zzzzzzzz for " + str(round(sleep_duration,0)) + " seconds" )
        time.sleep(sleep_duration)
    start_time = time.time()
    # print("Start time is " + str(start_time))
    # loop for index i to i + 600
    print("Instance: " + str(instance) + ". Run: " + str(rate_limit*(instance-1)) + " to " +  str(rate_limit*instance))
    for j in range(rate_limit*(instance-1),rate_limit*instance):
        print("Request number " + str(j))
        print("Requesting PDF for " + str(meta_working.at[j,'co_numb']))

        # Create request
        try:
            res = requests.get(meta_working.at[j,'doc_url'],headers=doc_headers)
        except requests.exceptions.ConnectionError as e:
            print("ERROR: " + str(e))

            log_list = []
            log_dict = {}
            log_dict['api_type'] = "pdf"
            log_dict['_error_message'] = str(e)
            log_dict['_url'] = meta_working.at[j,'co_numb']
            log_dict['_time'] = str(datetime.datetime.now())
            log_list.append(log_dict)
            # _error_message = str(e)
            # _url = metadata_master.at[j,'co_numb']
            # _time = str(datetime.datetime.now())
            # log_list = [_error_message,_url,_time]
            log_df = pd.DataFrame(log_list)
            log_df.to_csv(local.log_filepath/local.log_filename, index=False, mode='a')
            continue

        # Send request
        try:
            res.raise_for_status()
        except requests.exceptions.RequestException as e:
            print("ERROR: " + str(e))

            log_list = []
            log_dict = {}
            log_dict['api_type'] = "pdf"
            log_dict['_error_message'] = str(e)
            log_dict['_url'] = meta_working.at[j,'co_numb']
            log_dict['_time'] = str(datetime.datetime.now())
            log_list.append(log_dict)
            log_df = pd.DataFrame(log_list)
            log_df.to_csv(local.log_filepath/local.log_filename, index=False, mode='a')
            continue
        # print(res.headers)

        pdf_name = str(meta_working.at[j,'co_numb']) + "_" + meta_working.at[j,'category'] + "_" + str(meta_working.at[j,'date']) + ".pdf"

        # Get folder for PDF
        _dir_name = pdf_name[0:3]
        _destination_dir = destination_route_directory/_dir_name

        # Populate PDF
        with open(str(_destination_dir) +"/" + pdf_name,'wb') as f:
            f.write(res.content)

        # Once PDF has been downloaded, add URL to downloaded list
        # downloaded_urls_list.append(metadata_master.at[j,'doc_url'])

        # Change downloaded marker to 1
        metadata_master["downloaded"][metadata_master['doc_url'].str.match(meta_working.at[j,'doc_url'])] = 1

    # print("downloaded_urls_list has length: " + str(len(downloaded_urls_list)))
    # Convert list to pandas DataFrame
    # downloaded_urls_df = pd.DataFrame(downloaded_urls_list)
    # print("Downloaded URLs added to DF")
    # Append to existing output
    # downloaded_urls_df.to_csv(local.filepath_pdf_api/local.pdfs_downloaded_filename, index=False, mode='a')
    # print("Downloaded URLs DF added to CSV: " + str(local.filepath_pdf_api/local.pdfs_downloaded_filename))

    # Save co_numbs to file (so capture which ones downloaded in case it falls over )
    metadata_master.to_csv(local.meta_master)
    print("Updated metadata_master CSV")

    instance += 1
    end_time = time.time()
    instance_duration = end_time - start_time
    print("Instance duration is " + str(round(instance_duration,0)))

print("API calls finished")
