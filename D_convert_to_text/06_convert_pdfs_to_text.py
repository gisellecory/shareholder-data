# python3 03_convert_to_text/06_convert_pdfs_to_text.py

# (2) Convert PDFs to text data

from wand.image import Image
from PIL import Image as PI
import pyocr
import pyocr.builders
from pyocr import tesseract as tool
lang = tool.get_available_languages()[0] # print(tool.get_available_languages())

import time
import datetime
import io

import warnings
warnings.filterwarnings("ignore")
import pandas as pd

import shutil
import os
import glob

import sys
route_dir = "/Users/gisellecory/git/repo_shareholder_data"
sys.path.insert(0, route_dir)
import local

# Create current run output CSV if it doesn't exist
today = datetime.date.today()
text_output = str(local.text_route_file) + str(today) + ".csv"

if os.path.isfile(text_output) == False:
    print("Creating text output file")
    empty_text_df = pd.DataFrame(columns=["co_numb", "doc_url", "text"])
    empty_text_df.to_csv(text_output, index=False)
    # with open(text_output, 'w'):
        # pass

# Read in master metadata file
# was: co_numbs_with_urls
print("Reading in metadata_master")

metadata_master = pd.read_csv(local.meta_master, low_memory=False)

print("Length of metadata_master: " + str(len(metadata_master)))

metadata_master['downloaded'] = metadata_master['downloaded'].astype(int)

print(metadata_master.groupby(['downloaded']).size())

# Keep if downloaded == 1
metadata_master = metadata_master.loc[(metadata_master['downloaded'] == 1)]
print("Length after keeping downloaded only: " + str(len(metadata_master)))

# Keep if co_umbs in desired subset (if running v2 from scrath, this shouldn't be necessary)
# Create short co_numb for marking subset
metadata_master['co_numb_short'] = metadata_master['co_numb'].astype(str).str[0:2]

metadata_master = metadata_master.loc[(metadata_master['co_numb_short'] == '00') | (metadata_master['co_numb_short'] == "01") | (metadata_master['co_numb_short'] == "05") | (metadata_master['co_numb_short'] == "11") | (metadata_master['co_numb_short'] == "SC")]

print("Length after also keeping subset only: " + str(len(metadata_master)))

# Keep core columns
metadata_master = metadata_master[["co_numb","category","date","doc_url"]]

# Create index output CSV if it doesn't exist
if os.path.isfile(local.index_text_output) == False:
    print("Creating index text output file")
    empty_index_text_df = pd.DataFrame(columns=["doc_url"])
    empty_index_text_df.to_csv(local.index_text_output, index=False)
    # with open(local.index_text_output, 'w'):
        # pass
else:
    # If it does exist, read in the doc_urls and remove them from the metadata_master
    print("Reading in index text output file")
    index_df = pd.read_csv(local.index_text_output,low_memory=False)
    # merge with metadata_master
    metadata_master = metadata_master.merge(index_df, how="left", on="doc_url",indicator=True)
    print(metadata_master.groupby("_merge").count())
    # Keep only if not also in text_output_file
    # remove if _merge == both
    metadata_master = metadata_master.loc[(metadata_master['_merge'] != "both")]
    metadata_master.drop(['_merge'], axis=1, inplace=True)
    print("Length after removing those for which text has already been processed: " + str(len(metadata_master)))

# Remove duplicates
metadata_master.drop_duplicates(subset="doc_url",inplace=True)
print("Length after removing duplicates: " + str(len(metadata_master)))

# Sort by company number
metadata_master.sort_values(by=['co_numb'], inplace=True)
metadata_master = metadata_master.reset_index(drop=True)

# Start processing

instance = 1
instance_limit = 5


while instance <10000 :
    print("Instance: " + str(instance))
    start_time_instance = time.time()
    dict_list = []

     # For each row of metadata_master
    for j in range(instance_limit*(instance-1),instance_limit*instance):
        print("Index: " + str(j))
        start_time_individual = time.time()
        # Construct filepath and filename
        print(str(metadata_master.at[j,'doc_url']))
        print(str(metadata_master.at[j,'co_numb']))
        print(str(metadata_master.at[j,'category']))
        print(str(metadata_master.at[j,'date']))

        _name = str(metadata_master.at[j,'co_numb']) + "_" + str(metadata_master.at[j,'category']) + "_" + str(metadata_master.at[j,'date']) + ".pdf"

        # Get folder for PDF
        _dir = str(local.pdf_route_dir)+str(_name[0:3])

        _file = str(_dir) +"/" + str(_name)

        # Go to location and pick up PDF
        print("File to be converted: " + _file)

        # Process text
        req_image = []
        final_text = []

        image_pdf = Image(filename=_file, resolution=300)
        image_jpeg = image_pdf.convert('jpeg')

        for img in image_jpeg.sequence:
            img_page = Image(image=img)
            req_image.append(img_page.make_blob('jpeg'))

        error_flag = False
        for img in req_image:
            try:
                txt = tool.image_to_string(
                PI.open(io.BytesIO(img)),
                lang=lang,builder=pyocr.builders.TextBuilder()
            )
            except OSError as e:
                error_flag = True
                continue

            final_text.append(txt)

        if error_flag:
            continue

        print(final_text)
        print("File " + _file + " successfully converted")

        # Save URL and text to list
        dict={}
        dict['co_numb'] = metadata_master.at[j,'co_numb']
        dict['doc_url'] = metadata_master.at[j,'doc_url']
        dict['text'] = final_text
        dict_list.append(dict)

        end_time_individual = time.time()
        individual_duration = end_time_individual - start_time_individual
        print("Individual duration is " + str(round(individual_duration,0)))

    # Save list (of URL and text) to file
    text_df = pd.DataFrame(dict_list)
    text_df.to_csv(text_output, index=False, mode="a",header=False)
    print("New text appended to CSV: " + text_output)

    # Note duration
    end_time_instance = time.time()
    instance_duration = end_time_instance - start_time_instance
    print("Instance duration is " + str(round(instance_duration,0)))

    # Need to append URL (only) to the index file
    text_df = text_df[['doc_url']]
    text_df.to_csv(local.index_text_output, index=False, mode="a", header=False)
    print("URLs appended to index file")

    # Delete temp files

    temp_files = os.listdir(local.temp_dir)
    # If file names starts with "magick-", delete
    for _file in temp_files:
        if _file.startswith("magick-"):
            try:
                os.remove(_file)
                print("File removed: " + str(_file))
            except FileNotFoundError:
                pass

    instance += 1
    # NOTE: NOT SAVING A "PROCESSED" MARKER TO metadata_combined AS WORRIED TOO MANY PROGRAMMES AMENDING THAT FILE AT ONCE WILL CORRUPT IT. INSTEAD, WHEN START THIS MODULE, PULL IN URLS FROM THE TEXT OUTPUT FILE AND STRIKE THEM FROM THE 'TO PROCESS' LIST


    # Deal with fact headers come in to csv every time
    # Change URLs to just the dyanmic bit to save space (do this everywhere )
