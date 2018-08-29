import warnings
warnings.filterwarnings("ignore")
import pandas as pd
import os.path
from datetime import datetime
from pathlib import Path
import local

# Read in company numbers
co_numbs = pd.read_csv(local.co_numbs_fp/local.company_numbs_output_filename)
co_numbs.drop_duplicates(subset="co_numb",inplace=True)

co_numbs['co_numb_short'] = co_numbs['co_numb'].astype(str).str[0:2]

print(co_numbs.head())

print(co_numbs.groupby(['co_numb_short']).size())
