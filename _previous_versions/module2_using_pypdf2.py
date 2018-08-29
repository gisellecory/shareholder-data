# (2) Convert PDFs to text data

import re
import pandas as pd
import PyPDF2
import textract
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

filename_list = ["02576490","03729622","03807687","03830901","04192034","04744918","05292775"]

dict_list = []

for filename in filename_list:
    filename = "pdfs/" + filename + ".pdf"
    #open allows you to read the file
    pdfFileObj = open(filename,'rb')
    #The pdfReader variable is a readable object that will be parsed
    try:
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj, strict = False)
        # Find the number of pages
        num_pages = pdfReader.numPages
        count = 0
        text = ""

        #The while loop will read each page
        while count < num_pages:
            pageObj = pdfReader.getPage(count)
            count +=1
            text += pageObj.extractText()

        #This if statement exists to check if the above library returned words
        if text != "":
           text = text
           # print(text)
         #If the above returns as False, we run the OCR library textract
        else:
            # print("not text")
            text = textract.process(filename, method='tesseract', language='eng')
            # print(text)
            # Now we have a text variable which contains all the text derived from our PDF file
        # Now take this string and append to test_10.csv, on appropriate row
        # row['pdf_text'] = text
        # print(text)

        dict={}
        dict['filename'] = filename
        dict['text'] = text
        dict_list.append(dict)

    # PyPDF2.utils.PdfReadError: Could not find xref table at specified location
    except PyPDF2.utils.PdfReadError:
        dict={}
        dict['filename'] = filename
        dict['text'] = "PyPDF2.utils.PdfReadError"
        dict_list.append(dict)
    except ValueError:
        dict={}
        dict['filename'] = filename
        dict['text'] = "ValueError"
        dict_list.append(dict)

text_df = pd.DataFrame(dict_list)
text_df['shareholder_info'] = ""
text_df = text_df.replace({r'\r\n': ' '}, regex=True)

text_df.to_csv("text_test_8.csv", index=True)
