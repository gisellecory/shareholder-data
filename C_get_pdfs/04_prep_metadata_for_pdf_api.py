# python3 02_get_pdfs/04_prep_metadata_for_pdf_api.py

import warnings
warnings.filterwarnings("ignore")
import pandas as pd
import numpy as np
import glob
pd.set_option('display.max_columns', None)
from pathlib import Path
import shutil
import os

import sys
route_dir = "/Users/gisellecory/git/repo_shareholder_data"
sys.path.insert(0, route_dir)
import local

# File paths
source_files = os.listdir(local.local.source_meta_dir)

# Count number of unsorted CSVs
counter = len(glob.glob1(local.source_meta_dir,"*.csv"))
print("Number of CSVs in directory [" + str(local.source_meta_dir) + "]: " + str(counter))

# Read in master metadata file
metadata_master = pd.read_csv(local.meta_master, low_memory=False)
# metadata_master = pd.DataFrame(columns=["co_numb","category","date","doc_url"])
print(list(metadata_master))

# Go through each file in folder
for _filename in source_files:
    if _filename.endswith('.csv'):
        print("File found: " + str(_filename))
        # Open
        temp_df = pd.read_csv(str(local.source_meta_dir)+"/"+str(_filename), low_memory=False)
        print("File of length: " + str(len(temp_df)))

        # Do some basic cleansing
        # drop if count_items = count_items (these are duds)
        try:
            temp_df = temp_df[temp_df.count_items != "count_items"]
        except TypeError:
            # Continue would jump me out the loop, just want to skip it here
            pass

        # drop if url empty
        temp_df = temp_df[temp_df.url.notnull()]
        temp_df = temp_df[temp_df['url'] != "none found"]

        # convert date column into a datetime column
        temp_df['date_dt'] = pd.to_datetime(temp_df['date'], errors='coerce')

        # Add year column and convert to integers (from float)
        temp_df['year'] = temp_df['date_dt'].dt.year
        temp_df.year = temp_df.year.fillna(-1)
        temp_df.year = temp_df.year.astype(int)

        # Assees year distribution
        # print(temp_df.groupby(['year']).size())

        # Drop if on or before 2015
        print("Number of rows before removing those before 2015: " + str(len(temp_df)))
        temp_df = temp_df.loc[(temp_df.year >= 2015) | (temp_df.year == -1)]
        print("Number of rows for 2015 and after only: " + str(len(temp_df)))
        # print(temp_df.groupby(['year']).size())

        # Assees page_count distribution
        # print(temp_df.groupby(['page_count']).size())

        # Change page_count to integer
        temp_df.page_count = temp_df.page_count.replace('none found', -1)
        temp_df.page_count = temp_df.page_count.fillna(-1)
        temp_df.page_count = temp_df.page_count.astype(int)

        lessthan4pgs = temp_df.loc[(temp_df.page_count <= 3) & (temp_df.page_count != -1) ]
        # print("Number of docs (not just CS) with less than 4 pages: " + str(len(lessthan4pgs))) # 417328

        # Drop if confirmation statement with no changes and 3 pages or less long
        # i.e. keep rows if description != "confirmation-statement-with-no-updates") OR page_count > 3
        # print("Number of rows before removing CS with no changes, of 3 pages or less: " + str(len(temp_df))) # 2092344
        temp_df = temp_df[(temp_df.description != "confirmation-statement-with-no-updates") | (temp_df.page_count >= 4) | (temp_df.page_count == -1)]
        # print("Number of rows after: " + str(len(temp_df))) # 1811706, i.e. 280k change

        # If more than one AR in dataset, keep only the most recent
        subset_ar = temp_df.loc[ (temp_df.category == "annual-return") ]
        # print("Number of ARs: " + str(len(subset_ar)))
        most_recent_ar = subset_ar.groupby(['co_numb'])['year'].transform(max) == subset_ar['year']
        subset_ar = subset_ar[most_recent_ar]
        # print("Number of ARs after removing older ones: " + str(len(subset_ar)))

        # Then append back in with the CS data
        print("Total dataset size: " + str(len(temp_df)))
        subset_cs = temp_df.loc[ (temp_df.category == "confirmation-statement") ]
        print("Number of confirmation statements: " + str(len(subset_cs)))
        temp_df = subset_cs.append(subset_ar, ignore_index=True)
        print("New dataset size: " + str(len(temp_df)))
        # print(list(temp_df.columns.values))

        # Modify URL for use in second API call
        # We want "document_metadata" with "frontend-doc" changed to "document" "https://frontend-doc-api.companieshouse.gov.uk/document/n1EjP_MALLs8xZp5hs86iHcYDli0TE-n6t4HUDeZuq8". Note that documentation says this is link format but doesn't work: http://document-api.companieshouse.gov.uk/document/{id}/content
        temp_df = temp_df.replace({"frontend-doc":"document"}, regex=True)
        temp_df['doc_url'] = temp_df['url'] + "/content"
        # Create PDF download status column
        # temp_df['pdf_download'] = 0

        # Keep selected columns
        temp_df = temp_df[["co_numb","category","date","doc_url"]]
        temp_df["downloaded"] = 0

        # Add to metadata_master
        metadata_master = metadata_master.append(temp_df)
        print("Length of metadata_master: " + str(len(metadata_master)))
        # move original CSV when done
        shutil.move(str(local.local.source_meta_dir)+"/"+str(_filename), local.dest_meta_dir)
        print("Moved " + _filename)

print("metadata_master (pre dup removal) has length: " + str(len(metadata_master)))
# Remove duplicates
metadata_master.drop_duplicates(inplace=True)
print("metadata_master (post dup removal) has length: " + str(len(metadata_master)))

print(metadata_master.head())
print(list(metadata_master))
# Save metadata_master to file (overwrite)
metadata_master.to_csv(local.meta_master, index=False)

print("Done")
