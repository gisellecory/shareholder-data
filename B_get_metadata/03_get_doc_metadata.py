# python3 01_get_metadata/03_get_doc_metadata.py
# # # # # #
#  Get document IDs using CH document API
# # # # # #

import warnings
warnings.filterwarnings("ignore")
import pandas as pd
import os.path
import requests
from pprint import pprint as print
from IPython.display import JSON
# from datetime
import datetime
import time
import json
from pathlib import Path

import sys
route_dir = "/Users/gisellecory/git/repo_shareholder_data"
sys.path.insert(0, route_dir)
import local

# For timing
startTime = datetime.datetime.now()
print(startTime)
# print(datetime.time(datetime.now()))

today = datetime.date.today()
print(today)

metadata_output_file = str(meta_route_file) + str(today) + ".csv"
print(metadata_output_file)

# Create output CSV if it doesn't exist
if os.path.isfile(metadata_output_file) == False:
    with open(metadata_output_file, 'w'):
        pass

# Create log if it doesn't exist
if os.path.isfile(local.log_filepath/local.log_filename) == False:
    with open(local.log_filepath/local.log_filename, 'w'):
        pass

print("Loading in company numbers")
# Get co_numbs file
co_numbs = pd.read_csv(local.co_numbs_fp/local.co_numbs_all_fn, low_memory=False)

print(co_numbs.shape)
print(co_numbs.head())
print(list(co_numbs))
print(len(co_numbs))

# Order by company number
co_numbs.sort_values(by=['co_numb'], inplace=True)
co_numbs = co_numbs.reset_index(drop=True)

# Make into a list ONLY IF IN SUBSET AND DO NOT YET HAVE METADATA
print("Converting to list for those in subset without metadata already")
co_numbs_list = co_numbs[(co_numbs['subset'] == 1) & (co_numbs['metadata'] == 0)]
print(len(co_numbs_list))
co_numbs_list = co_numbs_list['co_numb'].tolist()
co_numbs_list.sort()

# Set global variables for API call
key = 'Basic dW9IWEViUzVhQUxIU3FyWTFxZ0YtMWxHRkVzU3VmenpvaGpDMDIwQg=='
gvChApi = "https://api.companieshouse.gov.uk/company"

# Set header
query_headers = {'Authorization': key}

instance = 1
rate_limit = 600

while instance < 7000:
    dict_list = []
    if instance != 1:
        # 301 instead of 300 just in case, and max to deal with negative times
        sleep_duration = max(0, 301 - instance_duration)
        # Take into account API rate limiting - wait 5 mins
        print("Sleeping zzzzzzzz for " + str(round(sleep_duration,0)) + " seconds")
        time.sleep(sleep_duration)
    start_time = time.time()
    # print("Start time is " + str(start_time))
    # loop for conumpany numbers index i to i + 600
    for j in range(rate_limit * (instance - 1), rate_limit * instance):
        # Set up and make call to document API

        # Create link, e.g.  https://api.companieshouse.gov.uk/company/{company_number}/filing-history
        query_url = gvChApi + "/" + \
            co_numbs_list[j] + "/filing-history?items_per_page=100&category=annual-return%2Cconfirmation-statement"

        print("Calling API instance #" + str(j))

        #  Create request
        try:
            res = requests.get(query_url, headers=query_headers)
        except requests.exceptions.ConnectionError as e:
            print("ERROR: " + str(e))

            log_list = []
            log_dict = {}
            log_dict['api_type'] = "metadata"
            log_dict['_error_message'] = str(e)
            log_dict['_co_numb'] = co_numbs_list[j]
            log_dict['_time'] = str(datetime.datetime.now())
            log_list.append(log_dict)
            log_df = pd.DataFrame(log_list)
            log_df.to_csv(local.log_filepath/local.log_filename, index=False, mode='a')
            continue

        #  Send request
        try:
            res.raise_for_status()
        except requests.exceptions.RequestException as e:
            print("ERROR: " + str(e))

            log_list = []
            # _error_message = str(e)
            # _co_numb = co_numbers[j]
            # _time = str(datetime.now())
            # log_list = [_error_message,_co_numb,_time]
            log_dict = {}
            log_dict['api_type'] = "metadata"
            log_dict['_error_message'] = str(e)
            log_dict['_co_numb'] = co_numbs_list[j]
            log_dict['_time'] = str(datetime.datetime.now())
            log_list.append(log_dict)
            log_df = pd.DataFrame(log_list)
            log_df.to_csv(local.log_filepath/local.log_filename, index=False, mode='a')
            continue

        json_output = res.json() # print(json_output['total_count'])

        # If success (data present)
        if (json_output['total_count'] != 0) and (json_output['total_count'] != "0"):
            # create a list of dictionaries (one per isntance)
            for i in range(len(json_output['items'])):
                if (json_output['items'][i]['description']) != "legacy":
                    dict = {}

                    # Number of items returned (should be the same for each item returned for a given company number)
                    dict['count_items'] = len(json_output['items'])

                    # Whole text
                    dict['json'] = json.dumps(json_output['items'][i])

                    # Company number
                    dict['co_numb'] = co_numbs_list[j]

                    # Category of filing
                    try:
                        dict['category'] = (json_output['items'][i]['category'])
                    except KeyError:
                        dict['category'] = ""

                    # Type of filing
                    try:
                        dict['type'] = (json_output['items'][i]['type'])
                    except KeyError:
                        dict['type'] = ""

                    # Description of filing
                    try:
                        dict['description'] = (json_output['items'][i]['description'])
                    except KeyError:
                        dict['description'] = ""

                    # Date (action date)
                    try:
                        dict['date'] = (json_output['items'][i]['action_date'])
                    except KeyError:
                        dict['date'] = ""

                    # Document URL
                    try:
                        dict['url'] = (json_output['items'][i]['links']['document_metadata'])
                    except KeyError:
                        dict['url'] = "none found"

                    # Page count of document
                    try:
                        dict['page_count'] = (json_output['items'][i]['pages'])
                    except KeyError:
                        dict['page_count'] = "none found"

                    # Whether paper filing
                    try:
                        dict['paper_filed'] = (json_output['items'][i]['paper_filed'])
                    except KeyError:
                        dict['paper_filed'] = ""

                    # Add dict to dict_list
                    dict_list.append(dict)

        # If no success
        elif json_output['total_count'] == 0:
            dict = {}
            dict['count_items'] = 0
            dict['json'] = ""
            dict['co_numb'] = co_numbs_list[j]
            dict['category'] = ""
            dict['type'] = ""
            dict['description'] = ""
            dict['date'] = ""
            dict['url'] = ""
            dict['page_count'] = ""
            dict['paper_filed'] = ""

            # Add dict to dict_list
            dict_list.append(dict)

            # Change metadata marker to 1
            co_numbs["metadata"][co_numbs['co_numb'].str.match(co_numbs_list[j])] = 1

        print("Finished collecting info for " + co_numbs_list[j])

    print("Converting new data from list to dataframe")
    # Convert list of dictionarties to pandas DataFrame
    output_df = pd.DataFrame(dict_list)

    # Reset indices
    # output_df = output_df.reset_index(drop=True)

    print("Appending new data to CSV: " + str(metadata_output_file))
    # Append to existing output
    output_df.to_csv(metadata_output_file, index=False, mode='a')

    # Save co_numbs to file (so capture which ones downloaded in case it falls over )
    co_numbs.to_csv(local.co_numbs_fp/local.co_numbs_all_fn)
    print("Updated co_numbs CSV")

    instance += 1
    end_time = time.time()
    # print("End time is " + str(end_time))
    instance_duration = end_time - start_time

print("API calls finished")

# Note timing
duration = datetime.now() - startTime
print(round(duration,0))
