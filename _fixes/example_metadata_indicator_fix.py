# # # # # #
# ONE TIME ONLY
# # # # # #

import warnings
warnings.filterwarnings("ignore")
import pandas as pd
import os.path
from datetime import datetime
from pathlib import Path
import local
import numpy as np

# Open up CSV of co-numbs that have metadata: co_numbs_with_metadata.csv
co_numbs_with_meta = pd.read_csv("/Users/gisellecory/Documents/dissertation_store/metadata/co_numbs_with_metadata.csv", low_memory=False)

# Merge with co_numbs
# Merge with outer join: Full outer join produces the set of all records in Table A and Table B, with matching records from both sides where available. If there is no match, the missing side will contain null.
co_numbs = pd.merge(co_numbs, co_numbs_with_meta, on='co_numb', how='outer', indicator=True)
print(co_numbs.groupby("_merge").count())

# Left only means only in co_numbs, not in metadata file: 3465990
# Right only means only in metadata file, not in co_numbs -> this is odd: 108891
# Both means in co_numbs and in metadata file: 770177

# If merge = right_only, drop
co_numbs = co_numbs[co_numbs['_merge'] != "right_only"]

# If _merge = both, then set metadata = 1
co_numbs["metadata"] = np.where(co_numbs['_merge'] == "both", 1,0)

# If merge = left_only, check metadata = 0
print(co_numbs.groupby("_merge").count())
print(co_numbs.groupby("subset").count())
print(co_numbs.groupby("metadata").count())

# Drop _merge
co_numbs.drop(['_merge'], axis=1, inplace=True)
print(list(co_numbs))
co_numbs['subset'] = co_numbs['subset'].astype(int)
print(co_numbs.dtypes)
print(co_numbs.groupby("subset").count())

# Save to file (overwrite)
print("Saving master file")
co_numbs.to_csv(local.co_numbs_fp/local.co_numbs_all_fn, index=False)
