# This is module 2 of 6
# This module reads in the master list of company numbers created in module 1 and requests metadata from the Companies House API for those for which metadata has not yet been gathered
# Created by Giselle Cory, 2018

# # # # # #
# # # # # #
# # # # # #
# Module 2: Get document IDs using Companies House API
# # # # # #
# # # # # #
# # # # # #

import pandas as pd
import numpy as np
import os.path
import requests
from pprint import pprint as print
from IPython.display import JSON
import datetime
import time
import json
import local_filepaths as fp

# For timing
startTime = datetime.datetime.now()

# Route for input to this module
co_numbs_file = fp.co_numbs_fp/fp.co_numbs_all_fn

# # # # # #
# Create filenames, files, and logs if needed
# # # # # #

# Create filename for current run of the module
today = datetime.date.today()
metadata_output_file = str(fp.meta_route_file) + str(today) + ".csv"
print(metadata_output_file)

# Create output CSV if it doesn't exist
if os.path.isfile(metadata_output_file) == False:
    with open(metadata_output_file, 'w'):
        pass

# Create log if it doesn't exist
if os.path.isfile(fp.log_filepath/fp.log_filename) == False:
    with open(fp.log_filepath/fp.log_filename, 'w'):
        pass

# # # # # #
# Read in data from CSV
# # # # # #

# Read in input CSV
print("Loading in company numbers")
co_numbs = pd.read_csv(co_numbs_file, dtype={'co_numb': object, 'subset': np.int32, 'metadata': np.int32}, low_memory=False)

# Assess data
print(co_numbs.shape)
print(co_numbs.head())
print(list(co_numbs))
print(len(co_numbs))

# Order by company number
co_numbs.sort_values(by=['co_numb'], inplace=True)
co_numbs = co_numbs.reset_index(drop=True)

# # # # # #
# Create list for use in API call
# # # # # #

# Take company numbers that are both in the subset and for which metadata has not yet been collected
# Make into a list
print("Converting to list for those in subset without metadata")
co_numbs_list = co_numbs[(co_numbs['subset'] == 1) & (co_numbs['metadata'] == 0)]
co_numbs_list = co_numbs_list['co_numb'].tolist()

# Order by company number (again - as action of converting to list can be distruptive)
co_numbs_list.sort()

# Check on size of list
print(len(co_numbs_list))

def ErrorLog(e,j):
    print("ERROR: " + str(e))
    log_list = []
    log_dict = {}
    log_dict['api_type'] = "metadata"
    log_dict['_error_message'] = str(e)
    log_dict['_co_numb'] = co_numbs_list[j]
    log_dict['_time'] = str(datetime.datetime.now())
    log_list.append(log_dict)
    log_df = pd.DataFrame(log_list)
    log_df.to_csv(fp.log_filepath/fp.log_filename, index=False, mode='a')

# # # # # #
# Set up API call
# # # # # #

# Set global variables for API call
key = ENTER-API-KEY-HERE
gvChApi = "https://api.companieshouse.gov.uk/company"
rate_limit = 600

# Set header
query_headers = {'Authorization': key}

instance = 1

# Set a safeguard to ensure programme terminates
while instance < 7000:

    # Create empty list. This will be used to placed the API results into, as dictionaries
    dict_list = []

    # If this is not the first instance, calculate time needed for pause so that rate limit is not exeeded
    if instance != 1:
        # Take the max to ensure no sleep negative durations
        sleep_duration = max(0, 301 - instance_duration)
        print("Sleeping zZzZ for " + str(round(sleep_duration,0)) + " seconds")
        # Sleep until 5 min period has ended
        time.sleep(sleep_duration)

    # Begin new instance
    instance_start_time = time.time()
    # This instance will loop over conumpany numbers i to i + 600
    for j in range(rate_limit * (instance - 1), rate_limit * instance):

        # Set up and make call to document API

        # Create link for API query
        # Format: https://api.companieshouse.gov.uk/company/{company_number}/filing-history
        query_url = str(gvChApi) + "/" + str(co_numbs_list[j]) + "/filing-history?items_per_page=100&category=annual-return%2Cconfirmation-statement"

        # Capture the time
        start_time_individual = time.time()
        start_time_to_display = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        print("Calling API instance #" + str(j))
        print("Started at: " + str(start_time_to_display))

        # # # # # #
        # Call API
        # # # # # #

        #  Send request to API
        try:
            res = requests.get(query_url, headers=query_headers)
        except requests.exceptions.ConnectionError as e:
             ErrorLog(e,j)
            continue
        try:
            res.raise_for_status()
        except requests.exceptions.RequestException as e:
            ErrorLog(e,j)
            continue

        # # # # # #
        # Capture returned data
        # # # # # #

        json_output = res.json()

        # If data present, create a list of dictionaries (one per isntance)
        if (json_output['total_count'] != 0) and (json_output['total_count'] != "0"):
            for i in range(len(json_output['items'])):
                if (json_output['items'][i]['description']) != "legacy":
                    dict = {}

                    # Count of items returned
                    dict['count_items'] = len(json_output['items'])

                    # Complete nested JSON element
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
                        dict['url'] = ""

                    # Page count of document
                    try:
                        dict['page_count'] = (json_output['items'][i]['pages'])
                    except KeyError:
                        dict['page_count'] = ""

                    # Whether paper filing
                    try:
                        dict['paper_filed'] = (json_output['items'][i]['paper_filed'])
                    except KeyError:
                        dict['paper_filed'] = ""

                    dict_list.append(dict)

        # If no data returned, create mostly empty dictionary:
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

            dict_list.append(dict)

        # # # # # #
        # Update metadata marker
        # # # # # #

        # Change metadata marker to 1
        co_numbs["metadata"][co_numbs['co_numb'].str.match(str(co_numbs_list[j]))] = 1
        print(co_numbs.groupby(['metadata']).size())

        # # # # # #
        # Note timing
        # # # # # #

        print("Finished collecting info for " + co_numbs_list[j])
        end_time_individual = time.time()
        individual_duration = end_time_individual - start_time_individual
        print("Individual duration is " + str(round(individual_duration,0)))

    # # # # # #
    # Save to file
    # # # # # #

    # Convert list of dictionarties to pandas DataFrame
    print("Converting new data from list to dataframe")
    output_df = pd.DataFrame(dict_list)

    print("Appending new data to CSV: " + str(metadata_output_file))
    # Append to existing output
    output_df.to_csv(metadata_output_file, index=False, mode='a')

    # Save co_numbs to file (to capture updated metadata markers)
    co_numbs.to_csv(co_numbs_file, index=False)
    print("Updated co_numbs CSV (of length: " + str(len(co_numbs)) + ")")

    # # # # # #
    # Note timing
    # # # # # #

    instance += 1
    instance_end_time = time.time()
    instance_duration = instance_end_time - instance_start_time
    print("Instance duration is " + str(round(instance_duration,0)))

print("API calls finished")
