# python3 A_setup/01_get_company_numbers_onefile.py

# # # # # #
# Get company numbers
# # # # # #

import warnings
warnings.filterwarnings("ignore")
import pandas as pd
from datetime import datetime
import numpy as np

# import os.path
# from pathlib import Path

import sys
route_dir = "/Users/gisellecory/git/repo_shareholder_data"
sys.path.insert(0, route_dir)
import local

# For timing
startTime = datetime.now()

# File paths
co_numbs_file = "/Users/gisellecory/Documents/dissertation_store/01_input_CH_data/co_numbs.csv"
ch_data = "/Users/gisellecory/Documents/dissertation_store/01_input_CH_data/BasicCompanyDataAsOneFile-2018-08-01.csv"

# Make sure that output CSV is empty to start with
f = open(co_numbs_file, "w+") # opening the file with w+ mode truncates the file
f.close()

# Open CH company numbers data (company numbers series only)
print("Reading in " + str(ch_data))
co_numbs = pd.read_csv(ch_data,low_memory=False, usecols= [' CompanyNumber'], dtype={' CompanyNumber': object})

# Rename series and save to CSV (for use in merge later on)
co_numbs = co_numbs.rename(columns={' CompanyNumber': 'co_numb'})
print("Number of company numbers in CH data: " + str(len(co_numbs)))

# Drop duplicates
co_numbs.drop_duplicates(subset="co_numb",inplace=True)
print(len(co_numbs))

# Create short co_numb for marking subset
co_numbs['co_numb_short'] = co_numbs['co_numb'].astype(str).str[0:2]

#  Create marker for subset of company numbers
co_numbs["subset"] = 0

# Change marker to 1 if company number starts with 00, 01,05,11 or SC
co_numbs['subset'] = ((co_numbs['co_numb_short'] == '00') | (co_numbs['co_numb_short'] == "01") | (co_numbs['co_numb_short'] == "05") | (co_numbs['co_numb_short'] == "11") | (co_numbs['co_numb_short'] == "SC")).astype(int)

# Drop temp series
co_numbs.drop(['co_numb_short'], axis=1, inplace=True)

# Assess subset
print(co_numbs.groupby("subset").count())

# Create marker for whether metadata gathered from API
co_numbs["metadata"] = 0

# Look
print(co_numbs.dtypes)
print(len(co_numbs))

# Save to file
co_numbs.to_csv(co_numbs_file, index=False)
print("Saved: " + str(co_numbs_file))

# Note timing
print(datetime.now() - startTime)
