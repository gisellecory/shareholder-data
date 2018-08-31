# # # # # #
# ONE TIME ONLY
# # # # # #

# Move PDFs from generic PDF store (which was too many files for finder) into sub-directories
# This is a one-off fix, as this is integrated into v2.0

import warnings
warnings.filterwarnings("ignore")
import pandas as pd

import shutil
import os
import glob
import local
import collections

# File paths
source_route_directory = local.filepath_pdf_store
source_files = os.listdir(source_route_directory)
destination_route_directory = local.filepath_pdf_directory

# Count number of unsorted PDFs
counter = len(glob.glob1(source_route_directory,"*.pdf"))
print("Number of PDFs in directory [" + str(source_route_directory) + "]: " + str(counter))

# Take a look at how many PDFs for each company number route (first 3 characters)
folder_name_list = []
for _filename in source_files:
    if _filename.endswith('.pdf'):
        _filename = _filename[0:3]
        folder_name_list.append(_filename)
counter=collections.Counter(folder_name_list)
# print(counter)

# Create a DF of the 'index' (first 3 characters of company number)
temp_df = pd.DataFrame.from_dict(counter, orient="index", columns=["file_name"]).reset_index()

# for each index in this DF, create a folder
for i in range(len(temp_df)):
    directory = temp_df['index'][i]
    if not os.path.exists(destination_route_directory/directory):
        os.mkdir(destination_route_directory/directory)

# for each file in route directory, move to appropriate new directory
for _filename in source_files:
    if _filename.endswith('.pdf'):
        _dir_name = _filename[0:3]
        _file_to_move = source_route_directory/_filename
        _file_to_move = str(_file_to_move)
        _destination_dir = destination_route_directory/_dir_name
        _destination_dir = str(_destination_dir)
        _destination_file = str(_destination_dir) + "/" + str(_filename)
        if os.path.isfile(_destination_file) == False:
            shutil.move(_file_to_move, _destination_dir)
            print("Moved " + _file_to_move + " to " + _destination_dir)
