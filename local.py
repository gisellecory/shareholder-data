# local locations

from pathlib import Path

# System
route_dir = "/Users/gisellecory/git/repo_shareholder_data"

# Inpt for creating master list of company numbers
ch_data_src_list = ["BasicCompanyData-2018-08-01-part1_5.csv","BasicCompanyData-2018-08-01-part2_5.csv","BasicCompanyData-2018-08-01-part3_5.csv","BasicCompanyData-2018-08-01-part4_5.csv","BasicCompanyData-2018-08-01-part5_5.csv"]

# Master list of company numbers
co_numbs_fp = Path("/Users/gisellecory/Documents/dissertation_store/01_input_CH_data/")
co_numbs_all_fn = "co_numbs.csv"

# Metadata output (route)
meta_route_file = "/Users/gisellecory/Documents/dissertation_store/metadata/original_output_to_merge/metadata_"

# Master metadata
meta_master = "/Users/gisellecory/Documents/dissertation_store/metadata/metadata_combined.csv"

# Text output (route)
text_route_file = "/Users/gisellecory/Documents/dissertation_store/text/text_output_"

# Index text output
index_text_output = "/Users/gisellecory/Documents/dissertation_store/text/index_text_output.csv"

# Error log
log_filepath = Path("/Users/gisellecory/Documents/dissertation_store/00_error_logs/")
log_filename = "error_log.csv"

# FOLDERS
# Metadata outputs - source folder
source_meta_dir = Path("/Users/gisellecory/Documents/dissertation_store/metadata/original_output_to_merge/")

# Metadata outputs - destination folder
dest_meta_dir = Path("/Users/gisellecory/Documents/dissertation_store/metadata/original_output_that_has_been_merged/")

# PDF route directory
pdf_route_dir = "/Users/gisellecory/Documents/dissertation_store/pdf_route_directory/"

# Temp store for text processing
temp_dir = "/private/var/folders/3l/vybyg9js3d7fr1mnxt5bd4tc0000gn/T"
