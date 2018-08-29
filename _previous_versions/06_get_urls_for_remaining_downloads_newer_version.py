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
import shutil

# Create output CSV if it doesn't exist
if os.path.isfile(local.filepath_pdf_api/local.pdfs_downloaded_filename) == False:
    with open(local.filepath_pdf_api/local.pdfs_downloaded_filename, 'w'):
        pass

# (1) Get the latest metadata file
new_metadata = pd.read_csv(local.filepath_finished_api_output/local.selected_url_output_filename, low_memory=False)
print("Most up to date metadata batch (selected, and including those already downloaded), length: " + str(len(new_metadata)))
# print(list(output_df))

# Get the to-download list (not yet updated with lastest run)
# DID THIS WITH pdfs_to_download_filename_fix ONE TIME GIVEN FILTERING FOR SUBSET, BUT DONT NEED TO DO THIS ANYMORE. ONE TIME ONLY.
to_download_df = pd.read_csv(local.filepath_pdf_api/local.pdfs_to_download_filename, low_memory=False)
print("Outdated dataset of remaining URLs for download (including some recently downloaded), length: " + str(len(output_df)))
# Drop _merge column
output_df.drop(['_merge'], axis=1, inplace=True)
# print(list(output_df))

# (2) add new metadata to 'to download' list
to_download_df = pd.merge(to_download_df, new_metadata, on=['doc_url'], how='outer',indicator=True)
# print(len(output_df))
# print(list(output_df))
print(to_download_df.groupby(['_merge']).size())
# Drop _merge column
to_download_df.drop(['_merge'], axis=1, inplace=True)

# Remove odd URLs
to_download_df = to_download_df[to_download_df['doc_url'] != "none found/content"]

print("Number of PDFs left to download (for which we have metadata): " + str(len(to_download_df)))
# print(list(output_df))

# Save CSV
to_download_df.to_csv(local.filepath_pdf_api/local.pdfs_to_download_filename, index=True)
print("Saved CSV: " + str(local.filepath_pdf_api/local.pdfs_to_download_filename))

# Move
_file_to_move = str(local.filepath_finished_api_output/local.selected_url_output_filename)
_destination_dir = str(local.filepath_complete)
shutil.move(_file_to_move, _destination_dir)
print("Moved " + str(_file_to_move) + " to " + str(_destination_dir))
