# Outdated: Changed approach away from burndown lists to binary indicators

# # # # # #
# Get list of URLs to call
# # # # # #

import warnings
warnings.filterwarnings("ignore")
import pandas as pd
from pprint import pprint as print
from datetime import datetime
import os.path
import time
from pathlib import Path
import local

# Create output CSV if it doesn't exist
if os.path.isfile(local.filepath_pdf_api/local.pdfs_downloaded_filename) == False:
    with open(local.filepath_pdf_api/local.pdfs_downloaded_filename, 'w'):
        pass

# (1) Get the most up to date metadata file
full_df = pd.read_csv(local.metadata_output_fp/local.selected_url_output_filename, low_memory=False)
print("Most up to date dataset of captured metadata (selected, and including those already downloaded), length: " + str(len(full_df)))
# print(list(output_df))

# Get the to-download list (not yet updated with lastest run)
# DID THIS WITH pdfs_to_download_filename_fix ONE TIME GIVEN FILTERING FOR SUBSET, BUT DONT NEED TO DO THIS ANYMORE. ONE TIME ONLY.
output_df = pd.read_csv(local.filepath_pdf_api/local.pdfs_to_download_filename, low_memory=False)
print("Outdated dataset of remaining URLs for download (including some recently downloaded), length: " + str(len(output_df)))
# Drop _merge column
output_df.drop(['_merge'], axis=1, inplace=True)
# print(list(output_df))

# Get the downloaded dataset
downloaded_df = pd.read_csv(local.filepath_pdf_api/local.pdfs_downloaded_filename, low_memory=False)
print("Number of PDF downloads so far: " + str(len(downloaded_df)))
# print(list(downloaded_df))

# (2) Check rows in output_df against downloaded_df.
# If row appears in downloaded_df, remove it from output_df
output_df = pd.merge(output_df, downloaded_df, on=['doc_url'], how='left',indicator=True)
# print(len(output_df))
# print(list(output_df))
print(output_df.groupby(['_merge']).size())
# keep if _merge is left only (or doc_url_y is NaN)
output_df = output_df.loc[output_df['_merge'] == 'left_only']

# Remove odd URLs
output_df = output_df[output_df['doc_url'] != "none found/content"]

print("Number of PDFs left to download (for which we have metadata): " + str(len(output_df)))
# print(list(output_df))

# Save CSV
output_df.to_csv(local.filepath_pdf_api/local.pdfs_to_download_filename, index=False)
print("Saved CSV: " + str(local.filepath_pdf_api/local.pdfs_to_download_filename))
