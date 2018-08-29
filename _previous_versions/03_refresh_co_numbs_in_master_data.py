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
import shutil

# For timing
startTime = datetime.now()

# Read in subset of CNs that do not yet have metadata
remaining_co_numbs = pd.read_csv(local.co_numbs_fp/local.co_numbs_rem_fn, low_memory=False)
print("remaining_co_numbs has length " + str(len(remaining_co_numbs)))
# Drop _merge column
remaining_co_numbs.drop(['_merge'], axis=1, inplace=True)

# If there is not an existing output file (from latest metadata API run - there is likely to be), then flag and stop
if os.path.isfile(local.metadata_temp_fp/local.metadata_temp_fn) == False:
    print("No new output to check")
# If there is, then read it in
else:
    print("Reading in latest metadata API output")
    output_df = pd.read_csv(local.metadata_temp_fp/local.metadata_temp_fn, low_memory=False, skiprows=11,skip_blank_lines=True, header=0, error_bad_lines=False)
    # Issue here
    # usecols=["co_numb"]
    # print(list(output_df))
    print("Latest metadata API output has length: " + str(len(output_df)))
    print(list(output_df))
    print(output_df.head())

    # Merge co_numbs and latest output file
    print("Merging remaining company numbers with latest metadata API output")
    merged_output = remaining_co_numbs.merge(output_df, how="left", on="co_numb",indicator=True)
    # Eyeball merge outcome
    print(merged_output.groupby(['_merge']).size())

    # Keep only rows without metadata
    merged_output = merged_output.loc[merged_output['_merge'] == 'left_only']
    # print(merged_output.shape)
    print("Number of company numbers that do not yet have metadata associated with them: " + str(len(merged_output)))
    # Drop _merge column
    # remaining_co_numbs.drop(['_merge'], axis=1, inplace=True)

    # Overwrite burn down list
    print("Saving to file (" + str(local.co_numbs_rem_fn) + ")")

    merged_output.to_csv(local.co_numbs_fp/local.co_numbs_rem_fn, index=False)
    # This gives us an updated file with company numbers that do not yet have data associated with them

    # Move temp API output to new location (to inidcate that it has been merged, and prevent programme from doing this action again)
    _file_to_move = str( local.metadata_temp_fp/local.metadata_temp_fn)
    _destination_dir = str(local.metadata_output_fp_used)
    shutil.move(_file_to_move, _destination_dir)
    print("Moved " +str( _file_to_move) + " to " + str(_destination_dir))

# Note timing
print(datetime.now() - startTime)
