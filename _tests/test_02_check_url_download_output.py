import warnings
warnings.filterwarnings("ignore")
import pandas as pd
import requests
from pprint import pprint as print
from IPython.display import JSON
from datetime import datetime
import json
import os.path
import time
from itertools import islice

urls = 'intermediate outputs/urls_only.csv'
output_downloaded_filename = 'intermediate outputs/urls_complete.csv'
temp_df = pd.read_csv(urls, low_memory=False)
print(temp_df.head(100))

print(list(temp_df))

# print(temp_df.groupby(['pdf_download']).size())
temp_df = temp_df.loc[temp_df.pdf_download == 1]
# print(temp_df.groupby(['pdf_download']).size())

temp_df = temp_df[['doc_url']]
print(list(temp_df))
temp_df.to_csv(output_downloaded_filename, index=False)

# This should just be a fix, not needed generally

all_docapi_output_filename = 'intermediate outputs/merged_output_urls.csv'

temp_df = pd.read_csv(all_docapi_output_filename, low_memory=False)
print(list(temp_df))
print(temp_df.head(5))

# print(temp_df.groupby(['pdf_download']).size())
