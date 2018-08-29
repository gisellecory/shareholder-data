

# TO SEE HOW MANY COMPANIES NUMBERS GIVEN BY CH
company_numbers_output_filename = "data/co_numbs.csv"
# 4.2m (all unique CNs)

# TO SEE WHAT METADATA HAS BEEN COLLECTED SO FAR (AFTER RUNNING MODULE 4):
all_docapi_output_filename = 'intermediate outputs/full_output_metadata_api.csv'
# 1.5m URLs, for 270k ish unique CNs

# TO SEE WHAT METADATA WE WANT TO COLLECT (OR HAVE) OVERALL:
selected_docapi_output_filename = 'intermediate outputs/selected_output_urls.csv'

# TO COUNT HOW MANY PDFS (URLS) HAVE BEEN DOWNLOADED
output_downloaded_filename = 'intermediate outputs/urls_complete.csv'
# 98k

# TO COUNT HOW MANY PDFS (URLS) STILL TO BE DOWNLOADED [GIVEN AMOUNT OF  METADATA COLLECTED AT THE TIME]
# NOTE: WHY DOES THIS HAVE SO MANY COLUMNS?
urls_to_download_filename = 'intermediate outputs/urls_to_download.csv'
# 1.3m

# TO COUNT HOW MANY CO NUMS STILL NEED METADATA
api_input_filename = "outputs/merged_input.csv"
# 4m
