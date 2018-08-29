# Checks that a sample co_numb from new output is not also in the previous output

import warnings
warnings.filterwarnings("ignore")
import pandas as pd

all_docapi_output_filename = 'intermediate outputs/full_output_metadata_api.csv'


temp = pd.read_csv(all_docapi_output_filename, low_memory=False)

print(list(temp.columns.values))

temp = temp[['co_numb','count_items']]

pd.set_option('display.max_columns', None)
print(temp.head())
print(temp.groupby(['count_items']).size())

print(temp.loc[temp['co_numb'] == "00074616"])
