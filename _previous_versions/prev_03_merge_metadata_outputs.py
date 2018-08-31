# # # # # #
#  Merged dataset for doc URLs
# # # # # #

import warnings
warnings.filterwarnings("ignore")
import pandas as pd
import numpy as np
from pathlib import Path
import local
import glob
import os
import shutil

# Get all CSV files in "04_url_api_output_to_be_merged" folder
os.chdir(local.metadata_temp_fp)
output_filename_list = []
for file in glob.glob("*.csv"):
    output_filename_list.append(file)
print("Found: " + str(len(output_filename_list)) + " file(s)")

# Merge them all into one output df
for i in range(len(output_filename_list)):
    temp_df = pd.read_csv(output_filename_list[i], low_memory=False, usecols=[""])
    print("Found " + str(output_filename_list[i]))
    output_df = output_df.append(temp_df)
    print("Appended " + str(output_filename_list[i]))
    # Move CSV
    source_file = str(local.metadata_temp_fp) + "/" + str(output_filename_list[i])
    shutil.move(source_file, local.metadata_output_fp_used)
    print("File moved - " + str(source_file))

# Drop row if count_items = 0
output_df = output_df[output_df.count_items != "0"]

# Append to full output dataset
output_df.to_csv(local.metadata_output_fp/local.metadata_output_fn, index=True, mode='a')
print("Saved CSV: " + str(local.metadata_output_fp/local.metadata_output_fn))
