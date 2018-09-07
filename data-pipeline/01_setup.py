# This is module 1 of 6, and must be run on initiation of the programme - one-time only
# This module reads in a CSV of data of companies registered in the UK, published by Companies House
# Source: http://download.companieshouse.gov.uk/en_output.html

# Created by Giselle Cory, 2018

# # # # # #
# # # # # #
# # # # # #
# Module 1: Create master list of company numbers
# # # # # #
# # # # # #
# # # # # #

import pandas as pd
from datetime import datetime
import numpy as np
import sys
import local_filepaths as fp

# For timing
startTime = datetime.now()

# Route for output of this module
co_numbs_file = fp.co_numbs_fp/fp.co_numbs_all_fn

# # # # # #
# Read in data from CSV
# # # # # #

# Make sure that output CSV is empty
f = open(co_numbs_file, "w+")
f.close()

# Open CH company numbers data (using the company numbers column only)
print("Reading in " + str(fp.ch_src_data))
co_numbs = pd.read_csv(fp.ch_src_data,low_memory=False, usecols= [' CompanyNumber'], dtype={' CompanyNumber': object})

# # # # # #
# Some minor housekeeping
# # # # # #

# Rename column
co_numbs = co_numbs.rename(columns={' CompanyNumber': 'co_numb'})
print("Number of companies in Companies House data: " + str(len(co_numbs)))

# Remove duplicates (NB: there should not be any, but done as a precaution)
co_numbs.drop_duplicates(subset="co_numb",inplace=True)
print("Number of companies following de-duplication" + str(len(co_numbs)))

# # # # # #
# Subset the data
# # # # # #

 # NB: Marking a subset of the data for use is required for the prototype
 # It would not be needed in a full implementation

# Create a 'short' co_numb using first three characters
# This is used for allocating companies to our subset
co_numbs['co_numb_short'] = co_numbs['co_numb'].astype(str).str[0:2]

#  Create marker for subset of company numbers
co_numbs["subset"] = 0

# Change subset marker to 1 if company number starts with 00, 01,05,11 or SC
co_numbs['subset'] = ((co_numbs['co_numb_short'] == '00') | (co_numbs['co_numb_short'] == "01") | (co_numbs['co_numb_short'] == "05") | (co_numbs['co_numb_short'] == "11") | (co_numbs['co_numb_short'] == "SC")).astype(int)

# Drop the 'short' co_numb column - it is not needed after subset has been created
co_numbs.drop(['co_numb_short'], axis=1, inplace=True)

# Look at the size of the subset
print(co_numbs.groupby("subset").count())

# # # # # #
# Create metadata marker
# # # # # #

# Create a marker for whether metadata has been gathered from API for this company
# For use in module 2
co_numbs["metadata"] = 0

# # # # # #
# Check and save to file
# # # # # #

# Make sure length and dtypes are in order
print(co_numbs.dtypes)
print(len(co_numbs))

# Save to file
co_numbs.to_csv(co_numbs_file, index=False)
print("Saved: " + str(co_numbs_file))

# Note timing
print(datetime.now() - startTime)
