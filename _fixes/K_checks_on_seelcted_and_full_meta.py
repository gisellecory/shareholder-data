# python3 _fixes/K_checks_on_seelcted_and_full_meta.py

import warnings
warnings.filterwarnings("ignore")
import pandas as pd
pd.set_option('display.max_columns', None)

metadata = "/Users/gisellecory/Documents/dissertation_store/metadata/temp_to_check_with_co_numbs.csv"

file_to_test = "/Users/gisellecory/Documents/dissertation_store/metadata/to_check/selected_250818.csv"

# Fine:
# full_190818_1.csv
# full_190818_2.csv
# selected_220818.csv

# Problematic - but we are ignoring this, settling for some duplication:
# full_230818.csv
# selected_250818.csv

temp_meta_df = pd.read_csv(metadata, low_memory=False)
print(temp_meta_df.shape)

test_df = pd.read_csv(file_to_test, low_memory=False)
print(test_df.shape)
print(test_df.dtypes)
test_df.co_numb = test_df.co_numb.astype(str)
print(test_df.head(100))

# Merge
# “Left outer join produces a complete set of records from Table A, with the matching records (where available) in Table B. If there is no match, the right side will contain null.”
test_df = test_df.merge(temp_meta_df, how="left", on="co_numb", indicator=True)

print(test_df.groupby(['_merge']).size())
# There should always be a match, i.e. no left only
