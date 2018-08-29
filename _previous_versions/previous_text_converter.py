# (2) Convert PDFs to text data

from wand.image import Image
from PIL import Image as PI
import pyocr
import pyocr.builders
import io
import pandas as pd
from pyocr import tesseract as tool
# print(tool.get_available_languages())
lang = tool.get_available_languages()[0]

# Get files from folder
filename_list = ["02576490","03729622","03807687","03830901","04192034","04744918","05292775"]
filename_list += ["05441352","05956237","06101485","06482095","06505026","06506412","06562775"]
filename_list += ["06586327","06602187","06616924","06630789","06643032","06665435","06739031"]
filename_list += ["06749847","06967502","07093260","07104655","07108559","07267363","07315875"]
filename_list += ["07375389","07443029","07466529","07481999","07482096","07554916","07597898"]
filename_list += ["07668475","07720601","07861671","08173479","08190761","08336078","08395513"]
filename_list += ["08576736","08704271","09609901"]

dict_list = []

# Change to list of company numbers with URLs attached to them
for co_numb in filename_list:
    _filename = "pdfs/" + co_numb + ".pdf"

    req_image = []
    final_text = []

    image_pdf = Image(filename=_filename, resolution=300)
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
    print(final_text)

    dict={}
    dict['filename'] = co_numb
    dict['text'] = final_text
    dict_list.append(dict)

text_df = pd.DataFrame(dict_list)
text_df.to_csv("text_test_11.csv", index=True)
