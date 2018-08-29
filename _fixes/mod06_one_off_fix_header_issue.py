# python3 03_convert_to_text/one_off_fix_header_issue.py

# This was a one off after I made module 6 with errors, so sorted it out with this. Main code now sorted so no longer need this fix

import warnings
warnings.filterwarnings("ignore")
import pandas as pd

# file = "/Users/gisellecory/Documents/dissertation_store/text/index_text_output.csv"
file = "/Users/gisellecory/Documents/dissertation_store/text/text_output_2018-08-28.csv"

test = pd.read_csv(file, low_memory=False)

print(len(test))
print(list(test))

# drop if doc_url == "doc_url"

test = test.loc[(test["doc_url"] != "doc_url")]
print(len(test))
test = test.loc[(test["co_numb"] != "co_numb")]
print(len(test))
test = test.loc[(test["text"] != "text")]
print(len(test))
print(list(test))

test.to_csv(file, index=False)
