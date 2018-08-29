# python3 _fixes/I_update_co_numbs_with_urls_urls_downloaded.py

import warnings
warnings.filterwarnings("ignore")
import pandas as pd
pd.set_option('display.max_columns', None)
import os.path

# Update meta master with previous URL download log files

master_file = "/Users/gisellecory/Documents/dissertation_store/metadata/metadata_combined.csv"

# Read in master_file.csv
master_file_df = pd.read_csv(master_file, low_memory=False)

print(master_file_df.head())
print(list(master_file_df))
print(len(master_file_df))

# Read in file to merge

# co_numbs_with_urls
# urls_complete

merge_file = "/Users/gisellecory/Documents/dissertation_store/metadata/temp3.csv"

merge_file_df = pd.read_csv(merge_file, low_memory=False)
print(merge_file_df.head())
print(list(merge_file_df))
print(len(merge_file_df))
print(merge_file_df.groupby("downloaded").count())

# Keep if downloaded
# df.loc[(df['column_name'] == some_value)]
merge_file_df = merge_file_df.loc[(merge_file_df['downloaded'] == 1)]

print(len(merge_file_df))
merge_file_df = merge_file_df[['doc_url']]

# Merge merge_file_df to master_file_df
print("Merging master_file_df and merge_file_df")
master_file_df = master_file_df.merge(merge_file_df, how="left", on="doc_url",indicator=True)
print(master_file_df.groupby("_merge").count())
print(master_file_df.groupby("downloaded").count())

# If _merge == both, downloaded = 1
master_file_df["downloaded"][master_file_df['_merge'] == "both"] = 1
master_file_df.drop(['_merge'], axis=1, inplace=True)
print(list(master_file_df))
print(len(master_file_df))

print(master_file_df.groupby("downloaded").count())
print(list(master_file_df))
# Save to file (overwrite metadata_master)
master_file_df.to_csv("/Users/gisellecory/Documents/dissertation_store/metadata/metadata_combined.csv",index=False)
