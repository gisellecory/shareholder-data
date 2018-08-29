# # # # # #
#  Summary stats
# # # # # #

import warnings
warnings.filterwarnings("ignore")
import pandas as pd
from pprint import pprint as print
pd.set_option('display.max_columns', None)
import local

# number of company numbers in burndown; and as % of total subset

total_numb_companies = pd.read_csv(local.co_numbs_fp/local.co_numbs_all_fn, low_memory=False)
print("Total number of companies in CH data: " + str(len(total_numb_companies)))

subset_numb_companies = pd.read_csv(local.co_numbs_fp/local.co_numbs_sub_fn, low_memory=False)
print("Subset number of companies in CH data: " + str(len(subset_numb_companies)))

remaining_companies = pd.read_csv(local.co_numbs_fp/local.co_numbs_rem_fn, low_memory=False)
print("Companies that do not yet have metadata associated with them: " + str(len(remaining_companies)))

print(str(len(remaining_companies)/len(subset_numb_companies)) + " to go")
