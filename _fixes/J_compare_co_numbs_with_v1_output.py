# python3 _fixes/compare_co_numbs_with_v1_output.py

import warnings
warnings.filterwarnings("ignore")
import pandas as pd

#  Get merged flattened metadata output
metadata = "/Users/gisellecory/Documents/dissertation_store/metadata/temp_to_check_with_co_numbs.csv"

temp_meta_df = pd.read_csv(metadata, low_memory=False)
print(temp_meta_df.shape)

# Get master company number file
co_numbs = "/Users/gisellecory/Documents/dissertation_store/01_input_CH_data/co_numbs.csv"

co_numbs_df = pd.read_csv(co_numbs, low_memory=False)
print(co_numbs_df.shape)

# Merge
co_numbs_df = co_numbs_df.merge(temp_meta_df, how="outer", on="co_numb", indicator=True)

print(co_numbs_df.groupby(['_merge']).size())
print(co_numbs_df.groupby(['metadata']).size())
# Left only: 3366127
# Both: 870040
# right_only: 1

# If merge = both, metadata = 1
co_numbs_df["metadata"][co_numbs_df['_merge'] == "both"] = 1
print(co_numbs_df.groupby(['metadata']).size())

# If _merge = right_only, drop
print(len(co_numbs_df))
co_numbs_df = co_numbs_df[co_numbs_df._merge != "right_only"]
print(len(co_numbs_df))

# Drop _merge
co_numbs_df.drop(['_merge'], axis=1, inplace=True)

# Save (overwrite)
co_numbs_df.to_csv(co_numbs,index=False)
