import pandas as pd
import re

mydict = {
"col_name"  : "shareholder_info",
"pattern"   : 'Statement of Capital \(Share Capital\)(.+)Authorisation'
}

# PATTERN = re.compile('Statement of Capital \(Share Capital\)(.+)Authorisation')
PATTERN = re.compile(mydict['pattern'])
PATTERN2 = re.compile('Number allotted\s*(\d+)')
PATTERN3 = re.compile('Aggregate nominal\s*\D*(\d+)')
PATTERN4 = re.compile('value\s+(\D+)\s+Currency')
PATTERN5 = re.compile('The details below relate to individuals / corporate bodies that were shareholders as at([^a-zA-Z]+)\D+')
PATTERN6 = re.compile('Name:*([\D\d]+)')
# Shareholding 1[-\w\s]+/

# 'Name(\w+\s+\w+)\s+w*s*Shareholding')

def isolate_sh_info(row):
    # Get text between "Statement of Capital" and "Authorisation"
    # pat = PATTERN.findall(row['text'])
    pat = PATTERN.findall(row['text'])
    return ''.join(pat).replace("\\n"," ")

# def run1():

# run1()

def isolate_numb_allotted(row):
    # Get text between "Name:" and "<br />"
    pat = PATTERN2.findall(row['shareholder_info'])
    return ''.join(pat)

def isolate_value(row):
    # Get text between "Name:" and "<br />"
    pat = PATTERN3.findall(row['shareholder_info'])
    return ''.join(pat)

def isolate_currency(row):
    # Get text between "Name:" and "<br />"
    pat = PATTERN4.findall(row['shareholder_info'])
    return ''.join(pat)

def isolate_date(row):
    # Get text between "Name:" and "<br />"
    pat = PATTERN5.findall(row['shareholder_info'])
    return ''.join(pat)

def isolate_shareholding1_name(row):
    # Get text between "Name:" and "<br />"
    pat = PATTERN6.findall(row['shareholder_info'])
    return ''.join(pat)

text_df = pd.read_csv("outputs/text_test_11.csv")
# print(type(text_df))

text_df['shareholder_info'] = text_df.apply(isolate_sh_info, axis=1)
text_df['numb_allotted'] = text_df.apply(isolate_numb_allotted, axis=1)
text_df['value'] = text_df.apply(isolate_value, axis=1)
text_df['currency'] = text_df.apply(isolate_currency, axis=1)
text_df['date'] = text_df.apply(isolate_date, axis=1)
text_df['shareholding1_name'] = text_df.apply(isolate_shareholding1_name, axis=1)

print(list(text_df.columns.values))
text_df.drop(['text'], axis=1, inplace=True)

text_df.to_csv("outputs/text_test_11_sh_4.csv", index=True, quotechar='"')
