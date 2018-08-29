# python3 _fixes/update_co_numbs_with_urls_temp3.py

import warnings
warnings.filterwarnings("ignore")
import pandas as pd
pd.set_option('display.max_columns', None)
import os.path

# Update co_numbs_with_urls with temp3

# Read in co_numbs_with_urls
metadata_master = pd.read_csv("/Users/gisellecory/Documents/dissertation_store/metadata/co_numbs_with_urls.csv", low_memory=False)

# print(metadata_master.head())
print(list(metadata_master))
print(len(metadata_master))

# Read in temp3
temp3 = pd.read_csv("/Users/gisellecory/Documents/dissertation_store/metadata/temp3.csv", low_memory=False)
# print(temp3.head())
print(list(temp3))
print(len(temp3))
temp3 = temp3[['doc_url']]

# Merge temp3 to co_numbs_with_urls
print("Merging co_numbs_with_urls and temp3")
metadata_master = metadata_master.merge(temp3, how="outer", on="doc_url",indicator=True)
print(metadata_master.groupby("_merge").count())
print(metadata_master.groupby("downloaded").count())

# If _merge == both, downloaded = 1
metadata_master["downloaded"][metadata_master['_merge'] == "both"] = 1
metadata_master.drop(['_merge'], axis=1, inplace=True)
print(list(metadata_master))
print(len(metadata_master))

print(metadata_master.groupby("downloaded").count())

# Save to file (overwrite metadata_master)
metadata_master.to_csv("/Users/gisellecory/Documents/dissertation_store/metadata/co_numbs_with_urls.csv",index=False)
