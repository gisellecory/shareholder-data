# # # # # #
# ONE TIME ONLY
# # # # # #

# python3 _fixes/A_co_numbs_that_have_meta.py

import warnings
warnings.filterwarnings("ignore")
import pandas as pd
import numpy as np
import glob
pd.set_option('display.max_columns', None)
from pathlib import Path
import shutil
import os

# import sys
# sys.path.insert(0, '/Users/gisellecory/Google Drive/02 Learning/13_Dissertation/code')
# import local

# File paths
source_route_directory = Path("/Users/gisellecory/Documents/dissertation_store/metadata/original_output/")
source_files = os.listdir(source_route_directory)
destination_route_directory = Path("/Users/gisellecory/Documents/dissertation_store/metadata/checked_original_output/")

# Count number of unsorted CSVs
counter = len(glob.glob1(source_route_directory,"*.csv"))
print("Number of CSVs in directory [" + str(source_route_directory) + "]: " + str(counter))

# Create empty DF
merged_df = pd.DataFrame(columns=["co_numb"])

# Go through each file in folder
for _filename in source_files:
    if _filename.endswith('.csv'):
        print("File found: " + str(_filename))
        # Open
        temp_df = pd.read_csv(str(source_route_directory)+"/"+str(_filename), low_memory=False)
        print("File of length (pre-dup removal): " + str(len(temp_df)))
        # Keep co_numb column
        temp_df = temp_df[['co_numb']]
        # Remove duplicates
        temp_df.drop_duplicates(subset="co_numb",inplace=True)
        print("File of length (post-dup removal): " + str(len(temp_df)))
        # Add to merged_df
        merged_df = merged_df.append(temp_df)
        print("Length of merged DF: " + str(len(merged_df)))
        # move original CSV when done
        shutil.move(str(source_route_directory)+"/"+str(_filename), destination_route_directory)
        print("Moved " + _filename)

print("Merged DF (pre dup removal) has length: " + str(len(merged_df)))
# Remove duplicates
merged_df.drop_duplicates(subset="co_numb",inplace=True)
print("Merged DF (post dup removal) has length: " + str(len(merged_df)))
# Save merged_df to file
merged_df.to_csv("/Users/gisellecory/Documents/dissertation_store/metadata/temp_to_check_with_co_numbs.csv", index=False)

print("Done")
# Compare this file against master co_numbs
# Change downloaded marker for ones that appear in both

# # # # # #
# Log output from running this file (one-time only)
# # # # # #

# Giselles-Air:code gisellecory$ python3 co_numbs_that_have_meta.py
# Number of CSVs in directory [/Users/gisellecory/Documents/dissertation_store/metadata/original_output]: 18
# File found: full_190818_1.csv
# File of length (pre-dup removal): 1553651
# File of length (post-dup removal): 274004
# Length of merged DF: 274004
# Moved full_190818_1.csv
# File found: metadata_220818.csv
# File of length (pre-dup removal): 666852
# File of length (post-dup removal): 76530
# Length of merged DF: 350534
# Moved metadata_220818.csv
# File found: selected_220818.csv
# File of length (pre-dup removal): 1064302
# File of length (post-dup removal): 485260
# Length of merged DF: 835794
# Moved selected_220818.csv
# File found: full_190818_2.csv
# File of length (pre-dup removal): 1650034
# File of length (post-dup removal): 325942
# Length of merged DF: 1161736
# Moved full_190818_2.csv
# File found: metadata_160818_2.csv
# File of length (pre-dup removal): 191975
# File of length (post-dup removal): 39487
# Length of merged DF: 1201223
# Moved metadata_160818_2.csv
# File found: metadata_160818_1.csv
# File of length (pre-dup removal): 403259
# File of length (post-dup removal): 73353
# Length of merged DF: 1274576
# Moved metadata_160818_1.csv
# File found: metadata_170818.csv
# File of length (pre-dup removal): 421119
# File of length (post-dup removal): 92484
# Length of merged DF: 1367060
# Moved metadata_170818.csv
# File found: metadata_200818.csv
# File of length (pre-dup removal): 1307476
# File of length (post-dup removal): 154330
# Length of merged DF: 1521390
# Moved metadata_200818.csv
# File found: selected_250818.csv
# File of length (pre-dup removal): 248518
# File of length (post-dup removal): 108858
# Length of merged DF: 1630248
# Moved selected_250818.csv
# File found: metadata_250818.csv
# File of length (pre-dup removal): 985937
# File of length (post-dup removal): 110494
# Length of merged DF: 1740742
# Moved metadata_250818.csv
# File found: metadata_210818_3.csv
# File of length (pre-dup removal): 1886
# File of length (post-dup removal): 1882
# Length of merged DF: 1742624
# Moved metadata_210818_3.csv
# File found: metadata_190818_1.csv
# File of length (pre-dup removal): 552169
# File of length (post-dup removal): 120621
# Length of merged DF: 1863245
# Moved metadata_190818_1.csv
# File found: metadata_240818.csv
# File of length (pre-dup removal): 1332209
# File of length (post-dup removal): 90737
# Length of merged DF: 1953982
# Moved metadata_240818.csv
# File found: metadata_210818_2.csv
# File of length (pre-dup removal): 237922
# File of length (post-dup removal): 36089
# Length of merged DF: 1990071
# Moved metadata_210818_2.csv
# File found: full_230818.csv
# File of length (pre-dup removal): 5515507
# File of length (post-dup removal): 513778
# Length of merged DF: 2503849
# Moved full_230818.csv
# File found: metadata_190818_2.csv
# File of length (pre-dup removal): 41513
# File of length (post-dup removal): 4424
# Length of merged DF: 2508273
# Moved metadata_190818_2.csv
# File found: metadata_210818_1.csv
# File of length (pre-dup removal): 628326
# File of length (post-dup removal): 79688
# Length of merged DF: 2587961
# Moved metadata_210818_1.csv
# File found: metadata_180818.csv
# File of length (pre-dup removal): 552169
# File of length (post-dup removal): 120621
# Length of merged DF: 2708582
# Moved metadata_180818.csv
# Merged DF (pre dup removal) has length: 2708582
# Merged DF (post dup removal) has length: 879069
# Done
# # # #
# When only what I suspected where the "original" outputs, there were 13 files:
# Merged DF (pre dup removal) has length: 1000740
# Merged DF (post dup removal) has length: 770178




# 28 Aug

# Number of CSVs in directory [/Users/gisellecory/Documents/dissertation_store/metadata/original_output]: 10
# File found: metadata_220818.csv
# File of length (pre-dup removal): 666852
# File of length (post-dup removal): 76530
# Length of merged DF: 76530
# Moved metadata_220818.csv
# File found: metadata_170818.csv
# File of length (pre-dup removal): 421119
# File of length (post-dup removal): 92484
# Length of merged DF: 169014
# Moved metadata_170818.csv
# File found: metadata_210818.csv
# File of length (pre-dup removal): 868134
# File of length (post-dup removal): 105181
# Length of merged DF: 274195
# Moved metadata_210818.csv
# File found: metadata_200818.csv
# File of length (pre-dup removal): 1307476
# File of length (post-dup removal): 154330
# Length of merged DF: 428525
# Moved metadata_200818.csv
# File found: metadata_160818.csv
# File of length (pre-dup removal): 595234
# File of length (post-dup removal): 112839
# Length of merged DF: 541364
# Moved metadata_160818.csv
# File found: metadata_250818.csv
# File of length (pre-dup removal): 985937
# File of length (post-dup removal): 110494
# Length of merged DF: 651858
# Moved metadata_250818.csv
# File found: metadata_240818.csv
# File of length (pre-dup removal): 1332209
# File of length (post-dup removal): 90737
# Length of merged DF: 742595
# Moved metadata_240818.csv
# File found: metadata_260818.csv
# File of length (pre-dup removal): 996502
# File of length (post-dup removal): 99864
# Length of merged DF: 842459
# Moved metadata_260818.csv
# File found: metadata_190818.csv
# File of length (pre-dup removal): 593682
# File of length (post-dup removal): 125040
# Length of merged DF: 967499
# Moved metadata_190818.csv
# File found: metadata_180818.csv
# File of length (pre-dup removal): 552169
# File of length (post-dup removal): 120621
# Length of merged DF: 1088120
# Moved metadata_180818.csv
# Merged DF (pre dup removal) has length: 1088120
# Merged DF (post dup removal) has length: 870041
# Done
# Giselles-MacBook-Air:code gisellecory$
