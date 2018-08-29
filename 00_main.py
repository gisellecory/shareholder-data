# # # # # #
# # # # # #
# # # # # #
# #  (1) - GET COMPANY NUMBER LIST FROM COMPANIES HOUSE
# # # # # #
# # # # # #
# # # # # #

python3 01_get_company_numbers.py
python3 02_select_subset_of_cns.py

# Get company numbers and save to file

# # # # # #
# # # # # #
# # # # # #
# #  (2) - REFRESH 'PENDING' INSTANCES -> GET SET OF COMPANY NUMBERS THAT STILL NEED METADATA
# # # # # #
# # # # # #
# # # # # #

python3 03_refresh_co_numbs_in_master_data.py

# NOTE: ON REFRESH, RUN MODULE 4 BEFORE MODULE 2

# Merge co_numbs and existing output file, keep only rows without doc_ids so far. This gives us our set of company numbers that still need data

# # # # # #
# # # # # #
# # # # # #
# #  (3) - CALL DOC API TO GET METADATA
# # # # # #
# # # # # #
# # # # # #

python3 04_get_doc_metadata.py

# NOTE: Change filename on refresh

# Load in Company numbers that still need data. Run them through the document API. Output for each run is a dictionary, which is appended to a list of dictionaries. This is covnerted to a DF and saved to file.

# # # # # #
# # # # # #
# # # # # #
# #  (4) - MERGE SEPERATE API OUTPUT DATASETS INTO ONE
# # # # # #
# # # # # #
# # # # # #

python3 04_create_merged_url_dataset.py

#  NOTE: REQUIRES MANUAL STEP (ADDING OUTPUT OF MODULE 3 INTO output_filename_list FOLDER)

# Get all CSV files that have not been merged into main output. Merge them all into one output df, and save to file.

# # # # # #
# # # # # #
# # # # # #
# #  (5) - KEEP ONLY ROWS (DOC URLS) FOR WHICH WE WANT THE PDF FROM THE MAIN API CALL
# # # # # #
# # # # # #
# # # # # #

python3 05_select_urls_for_pdf_download.py

# Read in all metadata output collected so far, and drop rows (i.e. doc URLs) we don't need, add PDF download column and save to file.
# NB We could have just not got these in the first place, but we might want the full data for other things later on, so we get it all just in case

# # # # # #
# # # # # #
# # # # # #
# #  (6) - REFRESH 'PENDING' INSTANCES -> GET LIST OF URLS FOR WHICH PDF HAS NOT YET BEEN DOWNLOADED
# # # # # #
# # # # # #
# # # # # #

python3 06_get_urls_for_remaining_downloads.py

# Get the most up to date meta data file, get the downloaded dataset, and keep only rows that do NOT appear in downloaded dataset, save to file.

# # # # # #
# # # # # #
# # # # # #
# #  (7) - RUN URLS THROUGH MAIN API AND UPDATE DOWNLOAD RECORD
# # # # # #
# # # # # #
# # # # # #

python3 07_download_pdfs.py

# Open up URLS to download, run them through the main API and get PDFs and add doc URL to downloaded DF and save to file.

# # # # # #
# # # # # #
# # # # # #
# #  (8)
# # # # # #
# # # # # #
# # # # # #

python3 08_convert_pdfs_to_text.py

# Convert PDFs to JPEG and OCR them
# Add text to DataFrame
# Connvert text to structured data

# # # # # #
# # # # # #
# # # # # #
# #  Tests
# # # # # #
# # # # # #
# # # # # #

python3 test_01_check_new_output.py
python3 test_02_check_url_download_output.py
python3 test_03_generic_csv_test.py
python3 test_04_moving_pdfs.py
