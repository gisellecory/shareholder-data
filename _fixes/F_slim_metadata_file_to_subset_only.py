# # # # # #
# ONE TIME ONLY
# # # # # #

# This is a one off fix, from v1.0 to v2.0
# It deals with the fact we moved from a full set of company numbers to wanting data only for a subset of company numbers. But we'd already collected metadata, so we slim down the metadata just to the subset so that we are then downloading only desired PDFs within that subset of company numbers

import warnings
warnings.filterwarnings("ignore")
import pandas as pd
from pprint import pprint as print
from datetime import datetime
import os.path
import time
from pathlib import Path
import local

temp_df = pd.read_csv(local.filepath_pdf_api/local.pdfs_to_download_filename, low_memory=False)

print(list(temp_df))
print(len(temp_df))

# Keep if company number starts with 00, 01,05,11 or SC
temp_df['co_numb_short'] = temp_df['co_numb'].astype(str).str[0:2]
temp_df = temp_df.loc[(temp_df['co_numb_short'] == '00') | (temp_df['co_numb_short'] == "01") | (temp_df['co_numb_short'] == "05") | (temp_df['co_numb_short'] == "11") | (temp_df['co_numb_short'] == "SC")]
temp_df.drop(['co_numb_short'], axis=1, inplace=True)
print("Number of company numbers in chosen subset: " + str(len(temp_df)))

temp_df.to_csv(local.filepath_pdf_api/local.pdfs_to_download_filename_fix, index=False)
