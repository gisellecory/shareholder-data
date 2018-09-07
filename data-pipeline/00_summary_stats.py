# # # # # #
#  Summary stats
# # # # # #

import pandas as pd
from pprint import pprint as print
pd.set_option('display.max_columns', None)
import numpy as np
import sys
import local_filepaths as fp

# # # # # #
# Company numbers with markers
# # # # # #

co_numbs_file = fp.co_numbs_fp/fp.co_numbs_all_fn

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

meta_master_df = pd.read_csv(fp.meta_master, dtype={'co_numb': object, 'downloaded': np.int32}, low_memory=False)
print(list(meta_master_df))

print("Total number of metadata items collected: " + str(len(meta_master_df)))
print("Total number of metadata items for which PDF has been downloaded:")
print(meta_master_df.groupby(['downloaded']).size())

# # # # # #
# Text output
# # # # # #

text_df = pd.read_csv(fp.text_combined, low_memory=False)

print("Total number of processed PDFs: " + str(len(text_df)))
print(list(text_df))

text_df.drop_duplicates(inplace=True)
print("Total number of processed PDFs after duplicates removed: " + str(len(text_df)))
