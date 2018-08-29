# # # # # #
# ONE TIME ONLY
# # # # # #

# This is a one-off module to sort out transition from v1.0 to v2.0

# make metadata_input_fn = co_numbs_rem_fn

import warnings
warnings.filterwarnings("ignore")
import pandas as pd
import os.path
from pathlib import Path
import local

# Remaining company numbers
test = pd.read_csv(local.co_numbs_fp/local.co_numbs_rem_fn, low_memory=False)

print(test.head())
print(list(test))
print(len(test))

# Original set (subset)
remaining_co_numbs = pd.read_csv(local.co_numbs_fp/local.co_numbs_sub_fn, low_memory=False)
# 1m companies (i.e. full)

print(remaining_co_numbs.head())
print(list(remaining_co_numbs))
print(len(remaining_co_numbs))

# Actual remaining set
actual_remaining_co_numbs = pd.read_csv(local.metadata_input_fp/local.metadata_input_fn, low_memory=False)
print(actual_remaining_co_numbs.head())
print(list(actual_remaining_co_numbs))
print(len(actual_remaining_co_numbs))
actual_remaining_co_numbs.drop(['_merge'], axis=1, inplace=True)

actual_remaining_co_numbs.to_csv(local.co_numbs_fp/local.co_numbs_rem_fn, index=False)
