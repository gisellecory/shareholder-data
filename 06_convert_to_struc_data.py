# This is module 6 of 6
# This module converts raw OCR text output into structured data using Regex
# Created by Giselle Cory, 2018

# # # # # #
# # # # # #
# # # # # #
# Module 6: Convert text to structured data
# # # # # #
# # # # # #
# # # # # #

import pandas as pd
import sys
import local_filepaths as fp
import re
pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', -1)
import numpy as np
import text_fcns as fcn

# # # # # #
#  Functions for converting text to structured data
# # # # # #

# Function to search for FDS phrase, case-insensitive

def PhraseFinder(a):
    a = a.lower()
    phrase = "full\s*details\s*of\s*shareholders"
    pattern_compile = re.compile(phrase)
    pattern_result = pattern_compile.findall(a)
    return pattern_result

# Function to get only shareholder-relevant text

def isolate_sh_info(row):
    option_below = "shown below"
    option_soc = "statement of capital (share capital)"
    option_soc_reg = "statement of capital \(share capital\)"
    option_fds = "full details of shareholders"
    option_psc = "persons with significant control"
    option_confirm_reg = "confirmation statement i conﬁrm"
    pat_capture = "(.+)"

    if row['text'].find(option_below) != -1:
        pat_p1 = option_below
    elif row['text'].find(option_soc) != -1:
        pat_p1 = option_soc_reg
    elif row['text'].find(option_fds) != -1:
        pat_p1 = option_fds
    else:
        pat_p1 = option_fds

    if row['category'] == "confirmation-statement":
        if option_psc in row['text']:
            pat_p2 = option_psc
        else:
            pat_p2 = option_confirm_reg

    elif row['category'] == "annual-return":
        pat_p2 = "authorisation\s*authenticated"

    pattern_to_find = pat_p1 + pat_capture + pat_p2
    pattern_compile = re.compile(pattern_to_find)
    pattern_result = pattern_compile.findall(row['text'])
    return ''.join(pattern_result).replace("\\n"," ")

# Function to remove empty list items

def RemoveEmptyItems(a):
    a = list(filter(None, a))
    return a

# Function to remove single letter list items

def RemoveSingleLetterItems(a):
    a = [item for item in a if len(item) > 1]
    return a

# Function to strip leading and trailing spaces

def striplist(a):
    return([x.strip() for x in a])

# Function to remove multiple spaces

def spaces(a):
    return [re.sub(r'\s{1,}', ' ', i) for i in a]

# Function to capitalise text

def capitalise(a):
    return [x.title() for x in a]

# Function to remove unwanted words

def removeWords(a):
    return [re.sub(r'class of shares|shareholding|shares|shareholders|dividends|ordinary|currency|gbp|nominal|aggregate|value|number allotted|annual return|confirmation statement|amount paid\s*per share|amount unpaid\s*per share|prescribed particulars|total number|full details', '', i) for i in a]

# Function to isolate shareholder names

def splitTerm(row):
    return (re.split("delimiter",row['shareholder_info']))

##########
# Read in data
##########

# Read in combined text output
combi_text = pd.read_csv(fp.text_combined, usecols=["url","text"], dtype={'co_numb':object})

# Read in master metadata file
metadata_master = pd.read_csv(fp.meta_master, dtype={'downloaded':np.int32, 'year':np.int32, 'co_numb':object, 'count_items':np.int32, 'page_count':np.int32}, usecols=['category', 'co_numb', 'count_items', 'date', 'page_count', 'year', 'url'], low_memory=False)

##########
# Basic cleaning
##########

# Replace \n with space
combi_text['text'] = [w.replace('\\n', ' ') for w in combi_text['text']]

# Replace multiple spaces with one space
combi_text['text'] = combi_text['text'].str.replace(r'\s+', ' ')

##########
# Create merged dataset for items that have text
##########

# Merge combined text output and metadata master
combi_text = combi_text.merge(metadata_master, how="left", on="url",indicator=True)

# Only keep if _merge == both
print(combi_text.groupby("_merge").count())
combi_text = combi_text.loc[(combi_text['_merge'] == "both")]
combi_text.drop(['_merge'], axis=1, inplace=True)

##########
# Select rows that have shareholder name information
##########

# Run function to determine if key phrase mentioned in text
combi_text['FDS'] = (combi_text.text.apply(fcn.PhraseFinder))

# Keep only if FDS phrase is present
print("Number of entries before FDS filter: " + str(len(combi_text)))
combi_text = combi_text[combi_text.FDS.str.len() > 0]
print("Number for which FDS is present: " + str(len(combi_text)))
combi_text.drop(['FDS'], axis=1, inplace=True)

##########
# Slim down text to relevant section only
##########

# Make all lower case
combi_text['text'] = combi_text['text'].str.lower()

# Keep only relevant sectons of text
# [We need not parse all the text. Remove generic text and sections we are not interested in]
combi_text['shareholder_info'] = combi_text.apply(fcn.isolate_sh_info, axis=1)

##########
# Parse text (as single string per document)
##########

# Remove all numbers
combi_text['shareholder_info'] = combi_text['shareholder_info'].str.replace(r'\d{0,}', '', regex=True)

# Remove superfluous grammar
combi_text['shareholder_info'] = combi_text['shareholder_info'].str.replace("'|‘", ' ',regex=True)
combi_text['shareholder_info'] = combi_text['shareholder_info'].str.replace(';|]|\[|"|,|:|£|\?|\.|%|—|_|-|[/]+', ' ', regex=True)

# Replace mutliple adjacenet spaces with a single space
combi_text['shareholder_info'] = combi_text['shareholder_info'].str.replace(r'\s{1,}', ' ', regex=True)

# Remove single letters from a given term
combi_text['shareholder_info'] = combi_text['shareholder_info'].str.replace(r'ordinary \w non voting gbp', 'ordinary non voting gbp', regex=True)

# Remove unncessary terms
combi_text['shareholder_info'] = combi_text['shareholder_info'].str.replace(r'held as at the date of this return|held as at the date of this confirmation statement', '', regex=True)

# Assign values to a list of terms for spliting the text into a list of names
split_terms_list = ["ordinary shares","ordinary stock shares  name","ordinary gbp","ordinary gbp shares","ordinary shares", "ordinary gbp shares shares","ordinary gbp shares", "ordinary shares of each","deferred shares","stock units shares","issued shares ","cumulative preference shares","cumulative preference gbp","cimjlative preference gbp","preference shares","ordinary non voting gbp"]

# Create 'delimiter' keyword from split word list items
after = "delimiter"
for term in split_terms_list:
    before = term
    combi_text['shareholder_info'] = combi_text['shareholder_info'].str.replace(before,after,regex=True)

# Remove Electonically filed.... phrase (also taking into account  common OCR errors)
combi_text['shareholder_info'] = combi_text['shareholder_info'].str.replace('electronically\s*fi*led\s*document\s*for\s*c\s*o*\s*mpany\s*number', ' ', regex=True)

# And 'End of' pre-fix
combi_text['shareholder_info'] = combi_text['shareholder_info'].str.replace('end\s+of', ' ', regex=True)

# Remove name / shareholder / shreholding terms
# (1)
combi_text['shareholder_info'] = combi_text['shareholder_info'].str.replace('(name\s*:*\s*shareholding\s*\d+\s*:*)+',' ', regex=True)
# (2)
combi_text['shareholder_info'] = combi_text['shareholder_info'].str.replace('(shareholding\s*\d+(\s+\d+)*:*\s*name\s*:*)+',' ', regex=True)
# (3)
combi_text['shareholder_info'] = combi_text['shareholder_info'].str.replace('name\s*:\s*shareholding\s*\d+\s*',' ', regex=True)
# (4)
combi_text['shareholder_info'] = combi_text['shareholder_info'].str.replace('shareholding\s*\d+\s*',' ', regex=True)
# (5)
combi_text['shareholder_info'] = combi_text['shareholder_info'].str.replace('n\s*ame:*',' ', regex=True)

# Remove 'company number' term
combi_text['shareholder_info'] = combi_text['shareholder_info'].str.replace('c\s*0m\s*party\s*number',' ', regex=True)

# Remove leading and trailing spaces
combi_text['shareholder_info'] = combi_text['shareholder_info'].str.strip()

# Remove 'page'
combi_text['shareholder_info'] = combi_text['shareholder_info'].str.replace(r'(page\s*\d*|page\-s\s*\d*)', ' ', regex=True)

# Remove "Transferred On"
combi_text['shareholder_info'] = combi_text['shareholder_info'].str.replace(r'transferred\s*on', 'delimiter', regex=True)

# Replace mutliple adjacenet spaces with a single space
combi_text['shareholder_info'] = combi_text['shareholder_info'].str.replace(r'\s{1,}', ' ', regex=True)

# Remove some unwanted phrases
combi_text['shareholder_info'] = combi_text['shareholder_info'].str.replace(r'the details below relate to individuals / corporate bodies that were shareholders as at|or that had ceased to be shareholders since the made up date of the previous|the company has indicated that there are no changes to shareholder details', '', regex=True)

# Replace mutliple adjacenet spaces with a single space
combi_text['shareholder_info'] = combi_text['shareholder_info'].str.replace(r'\s{1,}', ' ', regex=True)

##########
# Split text into list of names and parse
##########

# Split into list of names
combi_text['Names'] = combi_text.apply(fcn.splitTerm, axis=1)

# Remove unwanted words
combi_text['Names'] = combi_text.Names.apply(fcn.removeWords)

# Capitalise
combi_text['Names'] = combi_text.Names.apply(fcn.capitalise)

# Remove leading and trailing spaces
combi_text['Names'] = combi_text.Names.apply(fcn.striplist)

# Remove multiple spaces
combi_text['Names'] = combi_text.Names.apply(fcn.spaces)

# Remove single letter items
combi_text['Names'] = combi_text.Names.apply(fcn.RemoveSingleLetterItems)

# Remove empty list items
combi_text['Names'] = combi_text.Names.apply(fcn.RemoveEmptyItems)

# If names list is empty, drop row
print("Length before dropping rows without any parsed shareholder names" + str(len(combi_text)))
combi_text = combi_text[(combi_text.Names.str.len() != 0)]
print("Length after dropping rows without any parsed shareholder names" + str(len(combi_text)))

# Remove unwanted column
combi_text.drop(['shareholder_info','count_items','page_count','text'], axis=1, inplace=True)

print(list(combi_text))

# # # # # # # #
# Merge with co_numbs
# # # # # # # #

# Read in ch_data
ch_data_file = "/Users/gisellecory/Documents/dissertation_store/01_input_CH_data/BasicCompanyDataAsOneFile-2018-08-01.csv"
print("Reading in " + str(ch_data_file))
ch_data = pd.read_csv(ch_data_file,low_memory=False, usecols = ['CompanyName', ' CompanyNumber', 'RegAddress.AddressLine1', ' RegAddress.AddressLine2', 'RegAddress.PostTown', 'RegAddress.County', 'RegAddress.Country', 'RegAddress.PostCode', 'CompanyCategory', 'CountryOfOrigin', 'IncorporationDate', 'URI', 'ConfStmtNextDueDate'], dtype={' CompanyNumber': object})

# Rename columns
ch_data = ch_data.rename(columns={' CompanyNumber': 'co_numb','CompanyName':'CoName', 'RegAddress.AddressLine1':'Add1', ' RegAddress.AddressLine2':'Add2', 'RegAddress.PostTown':'Add3', 'RegAddress.County':'Add4', 'RegAddress.Country':'AddCountry', 'RegAddress.PostCode':'AddPC', 'CompanyCategory':'CoCat', 'CountryOfOrigin':'CountryOrigin', 'IncorporationDate':'Est', 'URI':'ChUri', 'ConfStmtNextDueDate':'NextCS'})

# Merge
combi_text = combi_text.merge(ch_data, how="left", on="co_numb",indicator=True)

# Only keep if _merge == both
print(combi_text.groupby("_merge").count())
combi_text = combi_text.loc[(combi_text['_merge'] == "both")]
combi_text.drop(['_merge'], axis=1, inplace=True)

# Some basic cleaning of address data
combi_text['Add1'] = combi_text['Add1'].str.replace(r',|\.', '', regex=True)
combi_text['Add1'] = combi_text['Add1'].str.title()
combi_text['Add2'] = combi_text['Add2'].str.replace(r',|\.', '', regex=True)
combi_text['Add2'] = combi_text['Add2'].str.title()
combi_text['Add3'] = combi_text['Add3'].str.replace(r',|\.', '', regex=True)
combi_text['Add3'] = combi_text['Add3'].str.title()
combi_text['Add4'] = combi_text['Add4'].str.replace(r',|\.', '', regex=True)
combi_text['Add4'] = combi_text['Add4'].str.title()
combi_text['AddCountry'] = combi_text['AddCountry'].str.replace(r',|\.', '', regex=True)
combi_text['AddCountry'] = combi_text['AddCountry'].str.title()

# Save to file (overwrite)
combi_text.to_csv(fp.final_output, index=False)
