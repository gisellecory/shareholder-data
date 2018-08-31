# Outdated: Code improved

# # # # # #
#  Convert PDFs to text data
# # # # # #

from wand.image import Image
from PIL import Image as PI
import pyocr
import pyocr.builders
from pyocr import tesseract as tool
lang = tool.get_available_languages()[0] # print(tool.get_available_languages())

import io

import warnings
warnings.filterwarnings("ignore")
import pandas as pd

import shutil
import os
import glob

text_output_filename = "text/text_1.csv"

source_path = "pdfs_01_todo/"
destination_path = "pdfs_01_used/"

source_files = os.listdir(source_path)
counter = len(glob.glob1(source_path,"*.pdf"))
print("Number of PDFs in directory [" + source_path + "]: " + str(counter))

dict_list = []

for _filename in source_files:
    if _filename.endswith('.pdf'): # because of .ds files

        print("File to be converted: " + _filename)
        _filepath = source_path + _filename

        req_image = []
        final_text = []

        image_pdf = Image(filename=_filepath, resolution=300)
        image_jpeg = image_pdf.convert('jpeg')

        for img in image_jpeg.sequence:
            img_page = Image(image=img)
            req_image.append(img_page.make_blob('jpeg'))

        for img in req_image:
            txt = tool.image_to_string(
                PI.open(io.BytesIO(img)),
                lang=lang,
                builder=pyocr.builders.TextBuilder()
            )
            final_text.append(txt)

        # print(final_text)
        print("File successfully converted")

        dict={}
        dict['filename'] = _filename
        dict['text'] = final_text
        dict_list.append(dict)

        shutil.move(source_path + _filename, destination_path)
        print("File moved - " + str(_filename))

text_df = pd.DataFrame(dict_list)
text_df.to_csv(text_output_filename, index=False)
print("New text appended to CSV: " + text_output_filename)
