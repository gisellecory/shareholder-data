# Read in metadata co_numbs, master co_numbs, merge so that have both metadata and subset markers

import warnings
warnings.filterwarnings("ignore")
import pandas as pd
import numpy as np
import glob
pd.set_option('display.max_columns', None)
from pathlib import Path
import local
import shutil
import os

# Get the list of co_numbs that have metadata
all_meta = pd.read_csv("/Users/gisellecory/Documents/dissertation_store/metadata/co_numbs_with_urls.csv",low_memory=False)
print("Number of metadata items collected: " + str(len(all_meta)))

# Get the list of co_numbs (as it has the subset marker)
co_numbs = pd.read_csv(local.co_numbs_fp/local.co_numbs_all_fn, low_memory=False)
print("Company numbers have legnth: " + str(len(co_numbs)))
co_numbs.drop(['Unnamed: 0'], axis=1, inplace=True)
# print(co_numbs.dtypes)

# Merge them
print("Merge in company numbers")
all_meta = pd.merge(all_meta, co_numbs, on='co_numb', how='left', indicator=True, validate="many_to_one")

print(all_meta.groupby("_merge").count())

# Keep metadata if within desired subset
all_meta = all_meta[all_meta['subset'] == 1]
print("Number of metadata items collceted for companies we are interested in: " + str(len(all_meta)))

# Correct dtypes
all_meta['subset'] = all_meta['subset'].astype(int)
all_meta['metadata'] = all_meta['metadata'].astype(int)
all_meta['downloaded'] = all_meta['downloaded'].astype(int)

# Drop _merge
all_meta.drop(['_merge'], axis=1, inplace=True)

# Compare this subset to the downloaded URLs file. Put a marker for those that have already been downloaded
downloaded_urls = pd.read_csv("/Users/gisellecory/Documents/dissertation_store/05_pdf_api/urls_complete.csv", low_memory=False)

# Merge all_meta with downloaded_urls
print("Merge in URL_downloaded list")
all_meta = pd.merge(all_meta, downloaded_urls, on='doc_url', how='left', indicator=True)
print(all_meta.groupby("_merge").count())
# print(list(all_meta))

# If _merge = both, downloaded = 1. Otherwise, = 0.
all_meta["downloaded"] = 0
all_meta["downloaded"][all_meta['_merge'] == "both"] = 1
print(all_meta.groupby("downloaded").count())

# Drop _merge
all_meta.drop(['_merge','Unnamed: 0'], axis=1, inplace=True)

print("Number of items of metadata downloaded, for companies of interest: " + str(all_meta['downloaded'][(all_meta['downloaded']==1)].count()))

 # Save to file
# We now have a subset of metadata which is for our subset of company numbers, with a download indicator
all_meta.to_csv("/Users/gisellecory/Documents/dissertation_store/metadata/temp3.csv", index=False)


# OUTPUT FROM RUNNING THIS MODULE 26/08

# Number of metadata items collected: 1739725
# Company numbers have legnth: 4236167
#
# Copmany numbers with some metadata but not in company number list: 248518
# Company numbers with metadata and in company number list: 1491207
#
# Number of metadata items collceted for companies we are interested in: 640215
#
# For companies of interest:
# Metadata not downloaded: 249333
# Metadata downloaded: 403967
