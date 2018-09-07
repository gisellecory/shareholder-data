# This is module 5 of 6
# This module takes as its input PDF files and outputs text. It uses the pyocr OCR Engine, a Python wrapper for tesseract
# Created by Giselle Cory, 2018

# # # # # #
# # # # # #
# # # # # #
# Module 5: Convert PDFs to text data
# # # # # #
# # # # # #
# # # # # #

from wand.image import Image
from PIL import Image as PI
import pyocr
import pyocr.builders
import io

from pyocr import tesseract as tool # tool = pyocr.get_available_tools()[0]
lang = tool.get_available_languages()[0]
import time
import datetime

import pandas as pd
pd.set_option('display.max_columns', None)
import numpy as np
import shutil
import os
import sys
import local_filepaths as fp

# # # # # #
#  Ascertain which PDFs are still to be processed
# # # # # #

# # # # # #
#  Read in metadata file
# # # # # #

# Read in master metadata file, call metadata_working to remind myself that this DF should not overwite metadata_master
print("Reading in metadata_working")
metadata_working = pd.read_csv(fp.meta_master, dtype={'downloaded':np.int32, 'year':np.int32, 'co_numb':object, 'count_items':np.int32, 'page_count':np.int32}, low_memory=False)

# Take a look
print("Length of metadata_working: " + str(len(metadata_working)))
print(metadata_working.groupby(['downloaded']).size())
print(metadata_working.dtypes)

# # # # # #
#  Select rows and columns of interest
# # # # # #

# Keep if downloaded == 1
metadata_working = metadata_working.loc[(metadata_working['downloaded'] == 1)]
print("Length after keeping downloaded only: " + str(len(metadata_working)))

# Keep if paper_filed != True
metadata_working = metadata_working.loc[(metadata_working['paper_filed'] != True)]

# Keep if co_unmb in desired subset
# NB: If running v2 of this programme from scrath, this step shouldn't be necessary
# Create short co_numb for marking subset
metadata_working['co_numb_short'] = metadata_working['co_numb'].astype(str).str[0:2]
# Keep only selected prefixes
metadata_working = metadata_working.loc[(metadata_working['co_numb_short'] == '00') | (metadata_working['co_numb_short'] == "01") | (metadata_working['co_numb_short'] == "05") | (metadata_working['co_numb_short'] == "11") | (metadata_working['co_numb_short'] == "SC")]

print("Length after also slimming down to subset: " + str(len(metadata_working)))

# Keep core columns only (for efficiency)
metadata_working = metadata_working[["co_numb","category","date","url"]]

# # # # # #
# Read in combined text output file and merge - if it exists
# # # # # #

if not os.path.isfile(fp.text_combined):
    print("No pre-existing text output file")
else:
    # If it does exist, read in the urls and remove them from the metadata_working
    print("Reading in text output file")
    combi_text_df = pd.read_csv(fp.text_combined, usecols=["url","text"], low_memory=False)
    # merge with metadata_working
    metadata_working = metadata_working.merge(combi_text_df, how="left", on="url",indicator=True)
    print(metadata_working.groupby("_merge").count())
    # Keep if _merge != both (i.e. if not in text_output_file)
    metadata_working = metadata_working.loc[(metadata_working['_merge'] != "both")]
    metadata_working.drop(['_merge'], axis=1, inplace=True)
    print("Length after removing those for which text has already been processed: " + str(len(metadata_working)))

# Remove duplicates
# NB: doing so here to capture dups both in the metdata and combined text files
metadata_working.drop_duplicates(subset="url",inplace=True)
print("Length after removing duplicates: " + str(len(metadata_working)))

# Sort by company number
metadata_working.sort_values(by=['co_numb'], inplace=True)
metadata_working = metadata_working.reset_index(drop=True)

# # # # # #
#  Text processing
# # # # # #

instance = 1
instance_limit = 3

while instance <10000 :
    print("Instance: " + str(instance))
    start_time_instance = time.time()
    dict_list = []

     # For each row of metadata_working
    for j in range(instance_limit*(instance-1),instance_limit*instance):

        # Note timing
        print("Index: " + str(j))
        start_time_individual = time.time()
        time_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print("Started at: " + str(time_now))

        # Construct filepath and filename
        print("URL: " + str(metadata_working.at[j,'url']))
        print("Company number: " + str(metadata_working.at[j,'co_numb']))
        print("Category: " + str(metadata_working.at[j,'category']))
        print("Date: " + str(metadata_working.at[j,'date']))

        # For file
        _name = str(metadata_working.at[j,'co_numb']) + "_" + str(metadata_working.at[j,'category']) + "_" + str(metadata_working.at[j,'date']) + ".pdf"

        # For folder
        _dir = str(fp.pdf_route_dir)+str(_name[0:3])

        # Complete path
        _file = str(_dir) +"/" + str(_name)

        # Go to location and pick up PDF
        print("#####################")
        print("File to be converted: " + _file)
        print("#####################")

        # Create an empty list to hold images
        req_image = []
        # Create an empty list to hold final text
        final_text = []

        # Process text
        try:
            # Open the PDF using wand
            image_pdf = Image(filename=_file, resolution=300)
        except Exception as e:
            # Go back to start of loop
            print("#####################")
            print("Error: image_pdf")
            print("#####################")
            continue

        # Convert PDF to JPEG using wand
        try:
            image_jpeg = image_pdf.convert('jpeg')
        except ValueError as e:
            continue

        # Use wand to convert each page in the PDF into an image blob
        # Loop over blobs
        for img in image_jpeg.sequence:
            img_page = Image(image=img)
            # append as a blob into the req_image list
            req_image.append(img_page.make_blob('jpeg'))

        # run OCR over the image blobs
        txt = ""
        for img in req_image:
            try:
                txt += tool.image_to_string(
                PI.open(io.BytesIO(img)),
                lang=lang,
                builder=pyocr.builders.TextBuilder()
                )
                error_flag = False
            except OSError as e:
                error_flag = True
                print("#####################")
                print("Error: txt")
                print("#####################")
            final_text.append(txt)

        if error_flag:
            continue

        print("#####################")
        print("TEXT FOUND:")
        print(final_text)
        print("#####################")
        print("File " + _file + " successfully converted")

        # Save URL and text to list
        dict={}
        dict['co_numb'] = metadata_working.at[j,'co_numb']
        dict['url'] = metadata_working.at[j,'url']
        dict['text'] = final_text
        dict_list.append(dict)

        # Note timing
        end_time_individual = time.time()
        individual_duration = end_time_individual - start_time_individual
        print("Individual duration is " + str(round(individual_duration,0)))

    # Save to dataframe
    text_df = pd.DataFrame(dict_list)
    print(list(text_df))

    # # # # # #
    # Save to file - backup only
    # # # # # #

    # Create current run output CSV if it doesn't exist
    today = datetime.date.today()
    indiv_text_output = str(fp.text_route_file) + str(today) + ".csv"

    # if text output file does not exist write header
    if not os.path.isfile(indiv_text_output):
        print("Creating backup day text output file")
        text_df.to_csv(indiv_text_output, index=False)
    else:
        # else it exists so append without writing the header
        text_df.to_csv(indiv_text_output, index=False, mode="a",header=False)
        print("New text appended to CSV: " + indiv_text_output)

    # # # # # #
    # Save to file - master (combined) version
    # # # # # #

    # Append to the master file
    if 'url' in text_df.columns:
        if not os.path.isfile(fp.text_combined):
            text_df.to_csv(fp.text_combined, index=False)
            print("New text output file; data saved to file")
        else:
            text_df.to_csv(fp.text_combined, index=False, mode="a", header=False)
            print("New data appended to master text file")

    # Note timing
    end_time_instance = time.time()
    instance_duration = end_time_instance - start_time_instance
    print("Instance duration is " + str(round(instance_duration,0)))

    # # # # # #
    # Delete magick files
    # # # # # #

    _folder = fp.temp_dir
    temp_files = os.listdir(_folder)
    print("Number of temp files to delete: " + str(len(temp_files)))

    for i in range(len(temp_files)):
        # Create full file path
        _name = os.path.join(_folder, temp_files[i])
        # If it is a file (not a directory or other item), delete it
        if os.path.isfile(_name):
            print("File found: " + str(_name))
            try:
                # Delete
                os.remove(_name)
                print("Deleted")
            except FileNotFoundError:
                print("Error - file could not be deleted")
                pass

        # If it is a folder starting with "tess_", delete it
        elif (_name.startswith("tess_")):
            try:
                shutil.rmtree(_name)
                print("Removed: " + str(_name))
            except OSError as e:
                print ("Error - can not delete folder")
                pass

    print("Instance complete")
    instance += 1

print("Done")
