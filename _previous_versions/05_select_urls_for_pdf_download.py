# # # # # #
#  Select which filing (PDF) to download (by selecting URL)
# # # # # #

import warnings
warnings.filterwarnings("ignore")
import pandas as pd
import numpy as np
import glob
pd.set_option('display.max_columns', None)
from pathlib import Path
import local
import shutil

# Read in latest API output metadata
output_df = pd.read_csv(local.metadata_output_fp_used/local.metadata_temp_fn, usecols= ['category', 'co_numb', 'count_items', 'date', 'description', 'page_count', 'paper_filed', 'type', 'url'], low_memory=False, skiprows=11,skip_blank_lines=True, header=0, error_bad_lines=False)

print("Original size: " + str(len(output_df)))

# drop if count_items = count_items (these are duds)
output_df = output_df[output_df.count_items != "count_items"]

# drop if url empty
# print((output_df['url'].isnull()).sum())
output_df = output_df[output_df.url.notnull()]
# print((output_df['url'].isnull()).sum())
# print(output_df.head(300))

# convert date column into a datetime column
output_df['date_dt'] = pd.to_datetime(output_df['date'], errors='coerce')
# print(output_df.head(50))

# Add year and month columns and convert to integers (from float)
output_df['year'], output_df['month'] = output_df['date_dt'].dt.year, output_df['date_dt'].dt.month
output_df.year = output_df.year.fillna(-1)
output_df.month = output_df.month.fillna(-1)
output_df.year = output_df.year.astype(int)
output_df.month = output_df.month.astype(int)

# print(output_df[['date','date_dt','year','month']].head(50))
# print(output_df[['date','year','month']].head(50))
# no_year = output_df.loc[ output_df.year == -1]
# print(no_year.head(50))

# Assees year distribution
print(output_df.groupby(['year']).size())

# Drop if on or before 2015
print("Number of rows before removing pre 2015: " + str(len(output_df)))
output_df = output_df.loc[(output_df.year >= 2015) | (output_df.year == -1)]
print("Number of rows 2015 onwards only: " + str(len(output_df)))
print(output_df.groupby(['year']).size())

# Assees page_count distribution
print(output_df.groupby(['page_count']).size())

# Change page_count to integer
output_df.page_count = output_df.page_count.replace('none found', -1)
output_df.page_count = output_df.page_count.fillna(-1)
output_df.page_count = output_df.page_count.astype(int)
# output_df.page_count = output_df.page_count.replace(-1, np.nan)

lessthan4pgs = output_df.loc[(output_df.page_count <= 3) & (output_df.page_count != -1) ]
print("Number of docs (not just CS) with less than 4 pages: " + str(len(lessthan4pgs))) # 417328

# Drop if confirmation statement with no changes and 3 pages or less long
# i.e. keep rows if description != "confirmation-statement-with-no-updates") OR page_count > 3
print("Number of rows before removing CS with no changes, of 3 pages or less: " + str(len(output_df))) # 2092344
output_df = output_df[(output_df.description != "confirmation-statement-with-no-updates") | (output_df.page_count >= 4) | (output_df.page_count == -1)]
print("Number of rows after: " + str(len(output_df))) # 1811706, i.e. 280k change

# If more than one AR in dataset, keep only the most recent
subset_ar = output_df.loc[ (output_df.category == "annual-return") ]
print("Number of ARs: " + str(len(subset_ar)))
most_recent_ar = subset_ar.groupby(['co_numb'])['year'].transform(max) == subset_ar['year']
subset_ar = subset_ar[most_recent_ar]
print("Number of ARs after removing older ones: " + str(len(subset_ar)))

# Then merge back in with the CS data
print("Total dataset size: " + str(len(output_df)))
subset_cs = output_df.loc[ (output_df.category == "confirmation-statement") ]
print("Number of CS docs: " + str(len(subset_cs)))
output_df = subset_cs.append(subset_ar, ignore_index=True)
print("Number of appended CS and AR docs: " + str(len(output_df)))
# print(output_df.head(250))
print(list(output_df.columns.values))

# Modify URL for use in second API call
# We want "document_metadata" with "frontend-doc" changed to "document" "https://frontend-doc-api.companieshouse.gov.uk/document/n1EjP_MALLs8xZp5hs86iHcYDli0TE-n6t4HUDeZuq8". Note that documentation says this is link format but doesn't work: http://document-api.companieshouse.gov.uk/document/{id}/content
output_df = output_df.replace({"frontend-doc":"document"}, regex=True)
output_df['doc_url'] = output_df['url'] + "/content"
# Create PDF download status column
output_df['pdf_download'] = 0

# Save cleansed data to new location
output_df.to_csv(local.filepath_finished_api_output/local.selected_url_output_filename, index=True)

print("Saved CSV: " + str(local.filepath_finished_api_output/local.selected_url_output_filename))

# Move original (uncleansed) data
_file_to_move = str(local.metadata_output_fp_used/local.metadata_temp_fn)
_destination_dir = str(local.filepath_complete)
shutil.move(_file_to_move, _destination_dir)
print("Moved " + str(_file_to_move) + " to " + str(_destination_dir))

# Slim down data for use in second API call
# url_df = output_df[['doc_url','category', 'co_numb', 'date']]
# url_df.to_csv(urls_only_filename, index=True)
# print("Saved CSV: " + str(urls_only_filename))
