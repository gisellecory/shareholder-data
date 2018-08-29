# Some to dos:
# Logic for Latest annual return unless… CS.
# flag for whether electronically filed or not - use only those that are?

import pandas as pd
import re

import sys
route_dir = "/Users/gisellecory/git/repo_shareholder_data"
sys.path.insert(0, route_dir)
import local


pattern_list = [
{
"col_name"  : "shareholder_info",
"pattern"   : 'Statement of Capital \(Share Capital\)(.+)Authorisation'
},{
"col_name"  : "shares_numb_allotted",
"col_name"  : "shares_numb_allotted",
"pattern"   : 'Number allotted\s*(\d+)'
},{
"col_name"  : "share_value",
"pattern"   : 'Aggregate nominal\s*\D*(\d+)'
},{
"col_name"  : "share_value_currency",
"pattern"   : 'value\s+(\D+)\s+Currency'
},{
"col_name"  : "as_of_date",
"pattern"   : 'The details below relate to individuals / corporate bodies that were shareholders as at([^a-zA-Z]+)\D+'
},{
"col_name"  : "shareholder1_name",
"pattern"   : 'Name:*([\D\d]+)'
}]

# For 'text' column

def isolate_sh_info(row):
    PATTERN = re.compile(pattern_list[0]["pattern"])
    # Get text between "Statement of Capital" and "Authorisation"
    pat = PATTERN.findall(row['text'])
    return ''.join(pat).replace("\\n"," ")

text_df = pd.read_csv("outputs/text_test_11.csv")
text_df['shareholder_info'] = text_df.apply(isolate_sh_info, axis=1)
# For efficiency (?)
text_df.drop(['text'], axis=1, inplace=True)

# For 'shareholder_info' column

for i in range(1,len(pattern_list)):
    # Range is from 1 as we have used item 0 above and no longer need it

    # Create empty column
    text_df[pattern_list[i]["col_name"]] = ""

    # Iterows isn't efficient according to this: https://medium.com/@rtjeannier/pandas-101-cont-9d061cb73bfc
    for row_index, row in text_df.iterrows():
        PATTERN = re.compile(pattern_list[i]["pattern"])
        pat = PATTERN.findall(row['shareholder_info'])
        text_df.at[row_index, pattern_list[i]["col_name"]] = ''.join(pat)

text_df.to_csv("outputs/text_test_11_sh_6.csv", index=False, quotechar='"')
