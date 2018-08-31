# python3 A_setup/02_select_subset_of_cns.py

# # # # # #
#  Create marker for subset of company numbers
# # # # # #

import warnings
warnings.filterwarnings("ignore")
import pandas as pd
import os.path
from datetime import datetime
from pathlib import Path
import numpy as np

import sys
route_dir = "/Users/gisellecory/git/repo_shareholder_data"
sys.path.insert(0, route_dir)
import local

# co_numbs_file = local.co_numbs_fp/local.co_numbs_all_fn
co_numbs_file = "/Users/gisellecory/Documents/dissertation_store/01_input_CH_data/co_numbs_onefile.csv"
# co_numbs_file = "/Users/gisellecory/Documents/dissertation_store/01_input_CH_data/co_numbs_rebuild_v2.csv"
# co_numbs_file_output = "/Users/gisellecory/Documents/dissertation_store/01_input_CH_data/co_numbs_rebuild_v2_2.csv"

# Read in company numbers
co_numbs = pd.read_csv(co_numbs_file, dtype={'co_numb': object})

# Take a look
print(co_numbs.dtypes)
print("Number of company numbers in CH data: " + str(len(co_numbs)))

# Create short co_numb for marking subset
co_numbs['co_numb_short'] = co_numbs['co_numb'].astype(str).str[0:2]

# Create marker
co_numbs["subset"] = 0

# Change marker to 1 if company number starts with 00, 01,05,11 or SC
co_numbs['subset'] = ((co_numbs['co_numb_short'] == '00') | (co_numbs['co_numb_short'] == "01") | (co_numbs['co_numb_short'] == "05") | (co_numbs['co_numb_short'] == "11") | (co_numbs['co_numb_short'] == "SC")).astype(int)

co_numbs.drop(['co_numb_short'], axis=1, inplace=True)
# print("Number of company numbers in chosen subset: " + str(len(co_numbs)))
print(co_numbs.groupby("subset").count())

# Create marker for whether metadata gathered from API
co_numbs["metadata"] = 0
print(co_numbs.dtypes)
print(len(co_numbs))
# Save to file (overwrite)
print("Saving master file")
co_numbs.to_csv(co_numbs_file, index=False)
