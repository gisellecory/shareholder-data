# python3 _fixes/0_sort_glithcy_metdaata_output.py

# # # # # #
# ONE TIME ONLY
# # # # # #

# Used for:
# metadata_180818 (pewviously v4)
# metadata_250818
# metadata_2018-08-26_1

import warnings
warnings.filterwarnings("ignore")
import pandas as pd
from pprint import pprint as print
pd.set_option('display.max_columns', None)

# Select which file to test
# file_to_test = "/Users/gisellecory/Documents/dissertation_store/metadata/original_output/metadata_250818.csv"
file_to_test = "/Users/gisellecory/Documents/dissertation_store/metadata/original_output/metadata_2018-08-26.csv"

# metadata_180818 (pewviously v4)
# Was having issues as first 2 lines were blank. Sorted with following:
# temp_df = pd.read_csv(file_to_test, low_memory=False, skiprows=2, header=0, skip_blank_lines=True)

# metadata_250818
# Was having issues as first 11 lines were blank. Sorted with following:
# Read in CSV
# temp_df = pd.read_csv(file_to_test, low_memory=False, skiprows=11, header=0, skip_blank_lines=True)

# metadata_2018-08-26_1 and metadata_2018-08-26.csv
# First 13 lines black
temp_df = pd.read_csv(file_to_test, low_memory=False, skiprows=13, header=0, skip_blank_lines=True)

# Save new CSV
temp_df.to_csv(file_to_test, index=False)
