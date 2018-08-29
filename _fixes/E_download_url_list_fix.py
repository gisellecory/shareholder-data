# Remove already downloaded URLs from the URLs to download list 

# # # # # #
# ONE TIME ONLY
# # # # # #

import warnings
warnings.filterwarnings("ignore")
import pandas as pd
import os.path
import requests
from pprint import pprint as print
import time
import datetime
import local

# Get list of downloaded URLs
urls_downloaded_df = pd.read_csv(local.filepath_pdf_api/local.pdfs_downloaded_filename, low_memory=False)

# Get list of URLs that have been collected but not downloaded
urls_to_download_df = pd.read_csv(local.filepath_pdf_api/local.pdfs_to_download_filename, low_memory=False)
# urls_to_download_df.drop(['_merge'], axis=1, inplace=True)

# print(list(urls_downloaded_df))
# print(list(urls_to_download_df))

# Merge them
merge_df = urls_to_download_df.merge(urls_downloaded_df, how="left", on="doc_url",indicator=True)
print(merge_df.groupby(['_merge']).size())

# Keep left merge only, i.e. those in urls_to_download_df that were not also in urls_downloaded_df
# Left outer join produces a complete set of records from Table A, with the matching records (where available) in Table B. If there is no match, the right side will contain null.
merge_df = merge_df.loc[merge_df['_merge'] == 'left_only']
merge_df.drop(['_merge'], axis=1, inplace=True)

# print(list(merge_df))
# print(len(merge_df))
# merge_df=merge_df[merge_df["co_numb"]!="SC602528"]
# print(len(merge_df))

# Save to pdfs_to_download_filename = 'urls_to_download.csv'
merge_df.to_csv(local.filepath_pdf_api/local.pdfs_to_download_filename, index=False)
