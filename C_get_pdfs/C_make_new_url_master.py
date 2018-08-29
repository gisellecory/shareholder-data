# python3 02_get_pdfs/C_make_new_url_master.py

# ONLY HAVE TO RUN THIS ONCE FOR TRANSITION FROM OLD CODE ---- BUT NEED TO SORT OUT HOW THIS FITS INTO NEW CODE, I.E. NEED TO CREATE THIS FILE SOMEWHERE

import warnings
warnings.filterwarnings("ignore")
import pandas as pd
import numpy as np
import glob
pd.set_option('display.max_columns', None)
from pathlib import Path
# import local
import shutil
import os

import sys
route_dir = "/Users/gisellecory/git/repo_shareholder_data"
sys.path.insert(0, route_dir)
import local

# File paths
source_route_directory = Path("/Users/gisellecory/Documents/dissertation_store/metadata/original_output_to_merge/")
source_files = os.listdir(source_route_directory)
destination_route_directory = Path("/Users/gisellecory/Documents/dissertation_store/metadata/original_output_that_has_been_merged/")

# Count number of unsorted CSVs
counter = len(glob.glob1(source_route_directory,"*.csv"))
print("Number of CSVs in directory [" + str(source_route_directory) + "]: " + str(counter))

# Create empty DF
merged_df = pd.DataFrame(columns=["co_numb","category","date","doc_url"])

# Go through each file in folder
for _filename in source_files:
    if _filename.endswith('.csv'):
        print("File found: " + str(_filename))
        # Open
        temp_df = pd.read_csv(str(source_route_directory)+"/"+str(_filename), low_memory=False)
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

        # Then merge back in with the CS data
        print("Total dataset size: " + str(len(temp_df)))
        subset_cs = temp_df.loc[ (temp_df.category == "confirmation-statement") ]
        print("Number of confirmation statements: " + str(len(subset_cs)))
        temp_df = subset_cs.append(subset_ar, ignore_index=True)
        print("New dataset size (to be added to metadata master file): " + str(len(temp_df)))
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

        # Add to merged_df
        merged_df = merged_df.append(temp_df)
        print("Length of merged DF: " + str(len(merged_df)))
        # move original CSV when done
        shutil.move(str(source_route_directory)+"/"+str(_filename), destination_route_directory)
        print("Moved " + _filename)

print("Merged DF (pre dup removal) has length: " + str(len(merged_df)))
# Remove duplicates
merged_df.drop_duplicates(inplace=True)
print("Merged DF (post dup removal) has length: " + str(len(merged_df)))
# Save merged_df to file
print(merged_df.head())
print(list(merged_df))
# co_numbs_with_urls
merged_df.to_csv(local.meta_master, index=False)

print("Done")

# 28 Aug 2018

# Number of CSVs in directory [/Users/gisellecory/Documents/dissertation_store/metadata/original_output_to_merge]: 10
# File found: metadata_220818.csv
# File of length: 666852
# Number of rows before removing those before 2015: 635029
# Number of rows for 2015 and after only: 256127
# Total dataset size: 195603
# Number of confirmation statements: 89571
# New dataset size (to be added to metadata master file): 160370
# Length of merged DF: 160370
# Moved metadata_220818.csv

# File found: metadata_170818.csv
# File of length: 421119
# Number of rows before removing those before 2015: 403912
# Number of rows for 2015 and after only: 224697
# Total dataset size: 164085
# Number of confirmation statements: 83854
# New dataset size (to be added to metadata master file): 138801
# Length of merged DF: 299171
# Moved metadata_170818.csv

# File found: metadata_210818.csv
# File of length: 868134
# Number of rows before removing those before 2015: 844670
# Number of rows for 2015 and after only: 340920
# Total dataset size: 264444
# Number of confirmation statements: 120542
# New dataset size (to be added to metadata master file): 214653
# Length of merged DF: 513824
# Moved metadata_210818.csv

# File found: metadata_200818.csv
# File of length: 1307476
# Number of rows before removing those before 2015: 1298190
# Number of rows for 2015 and after only: 509495
# Total dataset size: 396903
# Number of confirmation statements: 190129
# New dataset size (to be added to metadata master file): 334716
# Length of merged DF: 848540
# Moved metadata_200818.csv

# File found: metadata_160818.csv
# File of length: 595234
# Number of rows before removing those before 2015: 578211
# Number of rows for 2015 and after only: 298389
# Total dataset size: 218682
# Number of confirmation statements: 108228
# New dataset size (to be added to metadata master file): 183469
# Length of merged DF: 1032009
# Moved metadata_160818.csv

# File found: metadata_250818.csv
# File of length: 985937
# Number of rows before removing those before 2015: 985628
# Number of rows for 2015 and after only: 408797
# Total dataset size: 315214
# Number of confirmation statements: 138772
# New dataset size (to be added to metadata master file): 248518
# Length of merged DF: 1280527
# Moved metadata_250818.csv

# File found: metadata_240818.csv
# File of length: 1332209
# Number of rows before removing those before 2015: 1310459
# Number of rows for 2015 and after only: 530548
# Total dataset size: 406406
# Number of confirmation statements: 184842
# New dataset size (to be added to metadata master file): 330876
# Length of merged DF: 1611403
# Moved metadata_240818.csv

# File found: metadata_260818.csv
# File of length: 996502
# Number of rows before removing those before 2015: 991046
# Number of rows for 2015 and after only: 382484
# Total dataset size: 292746
# Number of confirmation statements: 140393
# New dataset size (to be added to metadata master file): 250959
# Length of merged DF: 1862362
# Moved metadata_260818.csv

# File found: metadata_190818.csv
# File of length: 593682
# Number of rows before removing those before 2015: 570975
# Number of rows for 2015 and after only: 310378
# Total dataset size: 228147
# Number of confirmation statements: 116082
# New dataset size (to be added to metadata master file): 192663
# Length of merged DF: 2055025
# Moved metadata_190818.csv

# File found: metadata_180818.csv
# File of length: 552169
# Number of rows before removing those before 2015: 529787
# Number of rows for 2015 and after only: 293901
# Total dataset size: 215200
# Number of confirmation statements: 110015
# New dataset size (to be added to metadata master file): 182044
# Length of merged DF: 2237069
# Moved metadata_180818.csv

# Merged DF (pre dup removal) has length: 2237069
# Merged DF (post dup removal) has length: 1703078
#                  category   co_numb        date  \
# 0  confirmation-statement  03026927  2017-02-27
# 1  confirmation-statement  03050852  2017-04-27
# 2  confirmation-statement  03050855  2017-04-27
# 3  confirmation-statement  03050860  2017-04-27
# 4  confirmation-statement  03050868  2017-04-27
#
#                                              doc_url  downloaded
# 0  https://document-api.companieshouse.gov.uk/doc...         0.0
# 1  https://document-api.companieshouse.gov.uk/doc...         0.0
# 2  https://document-api.companieshouse.gov.uk/doc...         0.0
# 3  https://document-api.companieshouse.gov.uk/doc...         0.0
# 4  https://document-api.companieshouse.gov.uk/doc...         0.0
# ['category', 'co_numb', 'date', 'doc_url', 'downloaded']
# Done
# Giselles-MacBook-Air:code gisellecory$
