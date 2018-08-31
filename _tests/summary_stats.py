# python3 _tests/summary_stats.py

# # # # # #
#  Summary stats
# # # # # #

import warnings
warnings.filterwarnings("ignore")
import pandas as pd
from pprint import pprint as print
pd.set_option('display.max_columns', None)
import numpy as np

import sys
route_dir = "/Users/gisellecory/git/repo_shareholder_data"
sys.path.insert(0, route_dir)
import local

# # # # # #
# Company numbers with markers
# # # # # #

co_numbs_file = "/Users/gisellecory/Documents/dissertation_store/01_input_CH_data/co_numbs.csv"

co_numbs = pd.read_csv(co_numbs_file, dtype={'co_numb': object, 'subset': np.int32, 'metadata': np.int32}, low_memory=False)

print("Total number of companies in CH data: " + str(len(co_numbs)))
print(list(co_numbs))
print("Total number of companies within and without subset")
print(co_numbs.groupby(['subset']).size())
print("Total number of companies that have metadata")
print(co_numbs.groupby(['metadata']).size())

# # # # # #
# Metadata
# # # # # #

meta_master_df = pd.read_csv(local.meta_master, dtype={'co_numb': object, 'downloaded': np.int32}, low_memory=False)
print(list(meta_master_df))

print("Total number of metadata items collected: " + str(len(meta_master_df)))
print("Total number of metadata items for which PDF has been downloaded:")
print(meta_master_df.groupby(['downloaded']).size())

# meta_master_df.drop(['Unnamed: 0', 'Unnamed: 0.1'], axis=1, inplace=True)
# meta_master_df.to_csv(local.meta_master, index=False)

# # # # # #
# Text output index
# # # # # #

index_text_df = pd.read_csv(local.index_text_output, low_memory=False)

print("Total number of processed PDFs: " + str(len(index_text_df)))
print(list(index_text_df))

index_text_df.drop_duplicates(inplace=True)
print("Length after duplicates removed" + str(len(index_text_df)))



# print(str(len(remaining_companies)/len(subset_numb_companies)) + " to go")
