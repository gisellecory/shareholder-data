# python3 _fixes/exploring_co_numbs_with_urls.py

import warnings
warnings.filterwarnings("ignore")
import pandas as pd
pd.set_option('display.max_columns', None)
pd.options.display.max_colwidth = 200
import os.path

metadata_master = pd.read_csv("/Users/gisellecory/Documents/dissertation_store/metadata/co_numbs_with_urls.csv", low_memory=False)
# urls_complete = pd.read_csv("/Users/gisellecory/Documents/dissertation_store/05_pdf_api/urls_complete.csv", low_memory=False)


# temp files for v1 to v2 fix/co_numbs_with_metadata

print(metadata_master.loc[metadata_master['co_numb'] == "00000529"])

# print(urls_complete.doc_url.loc[urls_complete['doc_url'] == "https://document-api.companieshouse.gov.uk/document/wkyG9FhCpETTamjMXwA9fCmTveNlBVGhkWgaa0i8vIo/content"])
