# python3 _fixes/rebuild_co_numbs.py

import warnings
warnings.filterwarnings("ignore")
import pandas as pd
import numpy as np

import sys
route_dir = "/Users/gisellecory/git/repo_shareholder_data"
sys.path.insert(0, route_dir)
import local

# Get master company number file
co_numbs_df = pd.read_csv(local.co_numbs_fp/local.co_numbs_all_fn, low_memory=False, dtype={'metadata': np.int32, 'subset': np.int32})
 # 'co_numb': object,

# Take a look
print(co_numbs_df.shape) # 3385545
print(co_numbs_df.dtypes)
print(list(co_numbs_df))
print(co_numbs_df.groupby(['metadata']).size()) # 813086
print(co_numbs_df.groupby(['subset']).size()) # 439495

# # Get rid of the unamed columns
co_numbs_df = co_numbs_df[['co_numb', 'subset', 'metadata']]
co_numbs_df.rename(columns={'subset': 'subset_corrupted'}, inplace=True)

# Get re-created co_numb file
rebuilt_co_numbs = "/Users/gisellecory/Documents/dissertation_store/01_input_CH_data/co_numbs_rebuild_v2_2.csv"

rebuilt_co_numbs_df = pd.read_csv(rebuilt_co_numbs, low_memory=False, dtype={'co_numb': object, 'metadata': np.int32, 'subset': np.int32})
# Drop metadata column (all zero)
rebuilt_co_numbs_df.drop(['metadata'], axis=1, inplace=True)

# Take a look
print(rebuilt_co_numbs_df.shape) # 4236170
print(list(rebuilt_co_numbs_df))
print(rebuilt_co_numbs_df.dtypes)

# Duplicate company number column
rebuilt_co_numbs_df['co_numb_original'] = rebuilt_co_numbs_df['co_numb']

# Remove leading zeros from company numbers
rebuilt_co_numbs_df['co_numb'] = rebuilt_co_numbs_df['co_numb'].map(lambda x: x.lstrip('0'))

# Recast co_numb as int
co_numbrebuilt_co_numbs_dfs_df['co_numb'] = rebuilt_co_numbs_df['co_numb'].astype(int)

rebuilt_co_numbs_df.rename(columns={'subset': 'subset_rebuilt'}, inplace=True)

# Merge master and rebuilt dataframes
co_numbs_df = co_numbs_df.merge(rebuilt_co_numbs_df, how="outer", on="co_numb", indicator=True)

print(co_numbs_df.groupby(['_merge']).size())
# left_only           0
# right_only     850625
# both          3385545
# Most are in both (phew) and some are just in the rebuilt version. Keep everything

# Drop merge indicator
co_numbs_df.drop(['_merge'], axis=1, inplace=True)
print(list(co_numbs_df))
print(len(co_numbs_df)) # 4236170
print(co_numbs_df.groupby(['metadata']).size())
print(co_numbs_df.groupby(['subset_corrupted']).size())
print(co_numbs_df.groupby(['subset_rebuilt']).size())

# print(pd.crosstab(co_numbs_df.subset_corrupted, co_numbs_df.subset_rebuilt, margins=True))

# Rename
co_numbs_df.rename(columns={'subset_rebuilt':'subset'}, inplace=True)
# Drop
co_numbs_df.drop(['subset_corrupted'], axis=1, inplace=True)

print(list(co_numbs_df))

# Save (overwrite)
_file = "/Users/gisellecory/Documents/dissertation_store/01_input_CH_data/co_numbs_rebuild_v2_3.csv"

# _file = local.co_numbs_fp/local.co_numbs_all_fn

co_numbs_df.to_csv(_file,index=False)
