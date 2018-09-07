# This is module 3 of 6
# This module prepares dataset for second API call
# Created by Giselle Cory, 2018

# # # # # #
# # # # # #
# # # # # #
# Module 3: Prepare metadata for document API
# # # # # #
# # # # # #
# # # # # #

import pandas as pd
import numpy as np
import glob
pd.set_option('display.max_columns', None)
import shutil
import os
import local_filepaths as fp

# File path for source data
source_files = os.listdir(fp.source_meta_dir)

# # # # # #
# Assess whether any files to merge
# # # # # #

# Count number of CSVs to be merged into master dataset
counter = len(glob.glob1(fp.source_meta_dir,"*.csv"))
print("Number of CSVs in directory [" + str(fp.source_meta_dir) + "]: " + str(counter))

if counter == 0:
    print("No files to merge. Exiting.")
    exit()

# # # # # #
# Read in master metadata, or create DataFrame if file doesn't exist
# # # # # #

# Create empty DF if master metadata CSV doesn't exist
if not os.path.isfile(fp.meta_master):
    print("No master metadata file found. Empty dataframe created.")
    metadata_master = pd.DataFrame(columns=["co_numb","category","date","url","count_items","description","page_count","paper_filed","type"])
else:
    # Read in master metadata file
    print("Reading in metadata_master CSV")
    metadata_master = pd.read_csv(fp.meta_master, dtype={'co_numb': object, 'downloaded': np.int32, 'category': object, 'url': object, 'date': object }, low_memory=False)
    print(list(metadata_master))

# # # # # #
# Add new files to master dataset
# # # # # #

# Go through each file in folder
for _filename in source_files:
    if _filename.endswith('.csv'):
        print("File found: " + str(_filename))
        # Open CSV
        temp_df = pd.read_csv(str(fp.source_meta_dir)+"/"+str(_filename), dtype={'co_numb': object, 'category': object, 'url': object, 'date': object, 'description': object, 'json': object, 'type': object, 'url': object, 'count_items': object}, usecols=['category', 'co_numb', 'count_items', 'date', 'description', 'page_count', 'paper_filed', 'type', 'url'], low_memory=False)
        print(list(temp_df))
        print("File of length: " + str(len(temp_df)))

        # Add downloaded marker (for use in module 4)
        temp_df["downloaded"] = 0

        # Append data to master dataset
        print("Appending to master dataset")
        metadata_master = metadata_master.append(temp_df)
        print("Length of metadata_master: " + str(len(metadata_master)))

        # Move original CSV into 'merged' folder
        shutil.move(str(fp.source_meta_dir)+"/"+str(_filename), fp.dest_meta_dir)
        print("Moved " + _filename)

print("##################")
print("Finished appending metadata_master")
print("##################")

print("Length of meta master: " + str(len(metadata_master)))

# # # # # #
# Clean master dataset
# # # # # #

# Remove duplicates
metadata_master.drop_duplicates(inplace=True)
print("Length of metadata_master after de-duplication: " + str(len(metadata_master)))

# Remove oddities, largely from earlier version of module that created some unwanted rows
metadata_master = metadata_master[metadata_master['category'] != "category"]
metadata_master = metadata_master[metadata_master.url.notnull()]
metadata_master = metadata_master[metadata_master['url'] != "none found"]

print("Length after removing dud rows: " + str(len(metadata_master)))

# Convert date column into a datetime column
metadata_master['date_dt'] = pd.to_datetime(metadata_master['date'], errors='coerce')

# Add year column and convert it to integer
metadata_master['year'] = metadata_master['date_dt'].dt.year
metadata_master.year = metadata_master.year.fillna(-1)
metadata_master.year = metadata_master.year.astype(int)
metadata_master.drop(['date_dt'], axis=1, inplace=True)

# Keep only dyanmic text in URL (to save space)
metadata_master = metadata_master.replace({"https://frontend-doc-api.companieshouse.gov.uk/document/":""}, regex=True)

# Change page_count to integer
metadata_master.page_count = metadata_master.page_count.replace('none found', -1)
metadata_master.page_count = metadata_master.page_count.fillna(-1)
metadata_master.page_count = metadata_master.page_count.astype(int)

# # # # # #
# Keep only rows that we want to send to document API
# # # # # #

# Drop if dated before 2015
metadata_master = metadata_master.loc[(metadata_master.year >= 2015) | (metadata_master.year == -1)]
print("Length after keeping only those from 2015 onwards: " + str(len(metadata_master)))

# Drop if document type is confirmation statement with no updates
metadata_master = metadata_master[(metadata_master.description != "confirmation-statement-with-no-updates")]

print("Length after removing confirmation-statement-with-no-updates: " + str(len(metadata_master)))

# # # # # #
# Keep most recent annual return only
# # # # # #

# Create subset with only anual returns
subset_ar = metadata_master.loc[ (metadata_master.category == "annual-return") ]
print("Number of annual returns: " + str(len(subset_ar)))

# Keep only most recent
most_recent_ar = subset_ar.groupby(['co_numb'])['year'].transform(max) == subset_ar['year']
subset_ar = subset_ar[most_recent_ar]
print("Number of annual returns, keeping the most up to date only: " + str(len(subset_ar)))

# Create subset with confirmation statements only
subset_cs = metadata_master.loc[ (metadata_master.category == "confirmation-statement") ]
print("Number of confirmation statements: " + str(len(subset_cs)))

# Append these two subsets to get a combined dataset
metadata_master = subset_cs.append(subset_ar, ignore_index=True)
print("Length of dataset for most recent annual returns and confirmation statements with updates or with no description given: " + str(len(metadata_master)))

# # # # # #
# Check and save 
# # # # # #

print(metadata_master.head())
print(list(metadata_master))
# Save metadata_master to file (overwriting previous version)
metadata_master.to_csv(fp.meta_master, index=False)

print("Done")
