# # # # # #
#  Refresh company number list in master dataset
# # # # # #

import warnings
warnings.filterwarnings("ignore")
import pandas as pd
import os.path
from datetime import datetime
from pathlib import Path
import local

# For timing
startTime = datetime.now()

# Read in subset of CNs
co_numbs = read_csv(local.co_numbs_fp/local.cn_subset_input_filename, low_memory=False)

# Make sure metadata_input_fn CSV is empty to start with
f = open(local.metadata_input_fp/local.metadata_input_fn, "w+") # opening the file with w+ mode truncates the file
f.close()

# If there is not an existing output file (from merge of metadata API runs - so there is likely to always be), then create one
if os.path.isfile(local.metadata_output_fp/local.metadata_output_fn) == False:
    print("Creating output file (metadata API has not yet been called)")
    output_df = pd.DataFrame(columns=["co_numb"])
else:
    print("Reading in full metadata API output")
    output_df = pd.read_csv(local.metadata_output_fp/local.metadata_output_fn, low_memory=False, usecols=["co_numb"])
    print("Full metadata API output has length: " + str(len(output_df)))
    # keep co_numbs only
    # output_df = output_df[['co_numb']]
    # remove duplicates
    # output_df.drop_duplicates(subset="co_numb",inplace=True)

# Merge co_numbs and existing output file (metadata_output_fn)
# Left join on co_numb
# (Does not merge back into co_numbs if already in output_df but not in co_numbs)
print("Merging company numbers with metadat API output")
merged_output = co_numbs.merge(output_df, how="left", on="co_numb",indicator=True)
# Eyeball merge outcome
print(merged_output.groupby(['_merge']).size())

# Keep only rows without doc_ids so far
# WRITEUP: In future, would want to check for updates instead
merged_output = merged_output.loc[merged_output['_merge'] == 'left_only']
print(merged_output.shape)
print("Number of company numbers that do not yet have metadata associated with them: " + str(len(merged_output)))

# Save
print("Saving to file")
merged_output.to_csv(local.metadata_input_fp/local.metadata_input_fn, index=False)
# This gives us a file with company numbers that do not yet have data associated with them

# Note timing
print(datetime.now() - startTime)
