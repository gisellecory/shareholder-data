# python3 _fixes/v1_v2_fix.py

# Used on:
# metadata_190818_1.csv # 552169
# metadata_190818_2.csv # 41513

# metadata_210818_1.csv # 628326
# metadata_210818_2.csv # 237922
# metadata_210818_3.csv # 1886

# metadata_160818_1.csv # 403259
# metadata_160818_2.csv # 191975

# metadata_2018-08-26_1.csv # 152534
# metadata_2018-08-26.csv # 843968

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

# metadata_2018-08-26_1.csv
file1 = "/Users/gisellecory/Documents/dissertation_store/metadata/original_output/metadata_2018-08-26_1.csv"

# metadata_2018-08-26.csv
file2 = "/Users/gisellecory/Documents/dissertation_store/metadata/original_output/metadata_2018-08-26.csv"

#
# file3 = "/Users/gisellecory/Documents/dissertation_store/metadata/original_output/metadata_210818_3.csv"

combined_file = "/Users/gisellecory/Documents/dissertation_store/metadata/original_output/metadata_260818.csv"

# Read in
temp1 = pd.read_csv(file1, low_memory=False)
temp2 = pd.read_csv(file2, low_memory=False)
# temp3 = pd.read_csv(file3, low_memory=False)

print(len(temp1))
print(list(temp1))
print(len(temp2))
print(list(temp2))
# print(len(temp3))
# print(list(temp3))

# # Remove unwanted columns
# temp1.drop(['Unnamed: 0'], axis=1, inplace=True)
temp2.drop(['Unnamed: 0'], axis=1, inplace=True)
# # temp3.drop(['Unnamed: 0'], axis=1, inplace=True)
#
# # Append
new = pd.concat([temp1,temp2])
# new = temp1.append(temp2, ignore_index=True)
print(len(new))
print(list(new))

new.to_csv(combined_file, index=False)
