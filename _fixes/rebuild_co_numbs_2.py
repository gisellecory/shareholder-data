# python3 _fixes/rebuild_co_numbs_2.py

import warnings
warnings.filterwarnings("ignore")
import pandas as pd
import numpy as np

import sys
route_dir = "/Users/gisellecory/git/repo_shareholder_data"
sys.path.insert(0, route_dir)
import local

# Get company numbers master dataset
co_numbs_file = "/Users/gisellecory/Documents/dissertation_store/01_input_CH_data/co_numbs_onefile.csv"
# co_numbs_file = local.co_numbs_fp/local.co_numbs_all_fn
co_numbs = pd.read_csv(co_numbs_file, dtype={'co_numb': object, 'subset': np.int32, 'metadata': np.int32},  low_memory=False)

# Take a look
print(co_numbs.shape) # 3385545
print(co_numbs.dtypes)
print(list(co_numbs))
print(co_numbs.groupby(['metadata']).size()) # 813086
print(co_numbs.groupby(['subset']).size()) # 439495

# Get metadata set
meta_file = "/Users/gisellecory/Documents/dissertation_store/metadata/metadata_combined.csv"
meta = pd.read_csv(meta_file, dtype={'co_numb': object}, usecols= ['co_numb'])

print(meta.shape) # 3385545
print(meta.dtypes)
print(list(meta))
# print(meta.groupby(['downloaded']).size()) # 813086

# remove duplicates of company numbers
print(len(meta))
meta.drop_duplicates(subset="co_numb",inplace=True)
print(len(meta))

# merge
co_numbs = co_numbs.merge(meta, how="outer", on="co_numb", indicator=True)

# check merge is ok
print(co_numbs.groupby(['_merge']).size())

# where _merge == both, set metadata == 1
print(co_numbs.groupby(['metadata']).size())
co_numbs["metadata"][co_numbs['_merge'] == "both"] = 1
print(co_numbs.groupby(['metadata']).size())

# Drop merge indicator
co_numbs.drop(['_merge'], axis=1, inplace=True)

print(co_numbs.shape) # 3385545
print(co_numbs.dtypes)
print(list(co_numbs))
print(co_numbs.groupby(['metadata']).size()) # 813086
print(co_numbs.groupby(['subset']).size()) # 439495
print(len(co_numbs))

# Save (overwrite)
print("Saving master file")
co_numbs.to_csv(co_numbs_file, index=False)
