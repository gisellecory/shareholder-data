# python3 _tests/test_03_generic_csv_test.py
# # # # # #
#  CSV content tests
# # # # # #

import warnings
warnings.filterwarnings("ignore")
import pandas as pd
from pprint import pprint as print
pd.set_option('display.max_columns', None)

import sys
sys.path.insert(0, '/Users/gisellecory/Google Drive/02 Learning/13_Dissertation/code')

import local

# Select which file to test
# file_to_test = "/Users/gisellecory/Documents/dissertation_store/01_input_CH_data/co_numbs.csv"
# file_to_test = "/Users/gisellecory/Documents/dissertation_store/metadata/co_numbs_with_metadata.csv"
file_to_test = "/Users/gisellecory/Documents/dissertation_store/metadata/original_output/metadata_2018-08-26_1.csv"
# file_to_test = "/Users/gisellecory/Documents/dissertation_store/metadata/co_numbs_with_urls.csv"
# local.filepath_pdf_api/local.pdfs_to_download_filename
file_to_test ="/Users/gisellecory/Documents/dissertation_store/metadata/temp files for v1 to v2 fix/co_numbs_with_metadata.csv"

temp_df = pd.read_csv(file_to_test, low_memory=False)
# temp_df.drop(['Unnamed: 0', 'Unnamed: 0.1'], axis=1, inplace=True)

# temp_df = temp_df[['co_numb','subset','metadata']]
# Save new CSV
# temp_df.to_csv(file_to_test, index=False)

# Look at categorical variables
# print(temp_df.groupby(['subset']).size())
# print(temp_df.groupby(['metadata']).size())

# Read in CSV
# temp_df = pd.read_csv(file_to_test, low_memory=False, skip_blank_lines=True)
# temp_df.sort_values(by=['co_numb'], inplace=True)
# temp_df = temp_df.sort_values('co_numb')

# Take a look
# print(temp_df.shape)
print(temp_df.head())
# print(temp_df.count()) # Values that are not none only
print(list(temp_df))
print(len(temp_df))
# temp_df.drop(['_merge'], axis=1, inplace=True)

# print(temp_df.loc[temp_df['co_numb'] == "00209074"])

# print(temp_df[temp_df['doc_url'].str.contains('00209074')])

# print(temp_df.describe())

# print(temp_df.loc[100:200])

# unique_values = len(temp_df.co_numb.unique())

# print("Number of unique values: " + str(unique_values))



# Check if headers are coming in as rows
# print(len(temp_df[(temp_df['category'] == 'category')]))

# Look at categorical variables
# print(temp_df.groupby(['pdf_download']).size())

# Slim down
# temp_df = temp_df[['doc_url']]

# Save new CSV
# temp_df.to_csv("doc_api_outputs/output_v4_new.csv", index=False)

# Remove unwanted columns
# temp_df.drop(['Unnamed: 0','Unnamed: 0.1','Unnamed: 0.1.1'], axis=1, inplace=True)

# Save new CSV
# temp_df.to_csv(all_docapi_output_filename, index=False)



# Checks that a sample co_numb from new output is not also in the previous output
# print(temp.loc[temp['co_numb'] == "00074616"])
