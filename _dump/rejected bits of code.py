
# The word_tokenize() function will break our text phrases into individual words
tokens = word_tokenize(text)
# Create a new list which contains punctuation we wish to clean
punctuations = ['(',')',';',':','[',']',',']
# We initialize the stopwords variable which is a list of words like #"The", "I", "and", etc. that don't hold much value as keywords
stop_words = stopwords.words('english')
#We create a list comprehension which only returns a list of words #that are NOT IN stop_words and NOT IN punctuations.
keywords = [word for word in tokens if not word in stop_words and not word in punctuations]

D4C arabic stuff
# from __future__ import unicode_literals
# https://github.com/deanmalmgren/textract/pull/76
# from textract.parsers.pdf_parser import Parser
arabic_text = Parser().extract('arabic_singlepage.pdf', method='tesseract', language='ara')

for numb in co_numb:
    # Select rows for each company number
    if trans_id_df.loc[trans_id_df['co_numb'] == numb]:
        recent_date = trans_id_df['date'].max()
        trans_id_df = trans_id_df.drop(trans_id_df[(trans_id_df.date !=recent_date) & (trans_id_df.co_numb == numb)].index)

print(json_output['items'][i])
transaction_id_list.append(json_output['items'][i]['transaction_id'])
date_list.append(json_output['items'][i]['date'])

# Create list of transaction ids for accounts category
    transaction_id_list = []
    date_list = []
    for i in range(len(json_output['items'])):
        if json_output['items'][i]['category'] == "accounts":
            print(json_output['items'][i])
            transaction_id_list.append(json_output['items'][i]['transaction_id'])
            date_list.append(json_output['items'][i]['date'])
    print(transaction_id_list)

# #create df
transaction_id_df = pd.DataFrame({'col':transaction_id_list})
print (len(transaction_id_df))

# # Remove duplicates
transaction_id_df.drop_duplicates(keep="first")
print (transaction_id_df)

# # Pick most recent
if json_output['items'][i]['date'] == most recent:

    for key, value in json_output.items():
        print('Key: %s' % key)
        print('Value: %s' % value)

# First level key is 'items'
# Second level key is "category"

    print(json_output['items']['action_date'])
    for i in range(10):
        items_1 = json_output.items[i].category
        print(items_1)
    JSON(json_output)

    var response_JSON = JSON.parse(xhttp.responseText);
    console.log(response_JSON);

    for (var i = 0; i < response_JSON.items.length; i++) {
      var doc_type = response_JSON.items[i].category;
      console.log(doc_type);

append 0 count items to most_recent_df
output_df = output_mr_df.append(dict_list_0, ignore_index=True, sort=True)


# If there are two items with same company number and date, pick the one with the most pages
def get_max_rows(df):
    B_maxes = df.groupby('co_numb')['page_count'].transform(max)
    return df[df['page_count'] == B_maxes]
output_mr_df = get_max_rows(output_mr_df)


# for each company number, find most recent date and keep only that entry
# https://stackoverflow.com/questions/15705630/python-getting-the-row-which-has-the-max-value-in-groups-using-groupby
most_recent_df = trans_id_df.groupby(
    ['co_numb'])['date'].transform(max) == trans_id_df['date']
output_mr_df = trans_id_df[most_recent_df]


# For testing purposes only
# merged_both_only = merged_output.loc[merged_output['_merge'] == 'both']
# merged_both_only.to_csv("outputs/merged_both_only.csv")

# print(co_numbs.shape)
# print(co_numbs.head(n=20))

# Check if there is an existing output file
# if os.path.isfile(output_filename_list[0]) == True:
#     print("Found " + str(output_filename_list[0]))
#     output_df = pd.read_csv(output_filename_list[0], low_memory=False)
#     if len(output_filename_list) > 1:
#         for i in range(1,len(output_filename_list)):
#             # If so, read in existing (output) CSV
#             print("Found " + str(output_filename_list[i]))
#             _df_name = "output_df_" + str(i)
#             _df_name = pd.read_csv(output_filename_list[i], low_memory=False)
#             output_df = output_df.append(_df_name)
# else:
#     # If not, create empty DataFrame
#     output_df = pd.DataFrame(columns=["co_numb"])

# output_filename_list = ["doc_api_outputs/output_v1.csv", "doc_api_outputs/output_v2.csv","doc_api_outputs/output_v3.csv"]

# print(merged_output.describe())

# merged_output_filename = 'doc_api_outputs/merged_output_urls.csv'

output_df = output_df.loc[output_df.pdf_download == 0]
# downloaded_df.drop('pdf_download', axis=1)

merged_output_filename = 'intermediate outputs/merged_output_urls.csv'
temp_df = pd.read_csv(merged_output_filename, low_memory=False)
print(temp_df.head(100))
print(list(temp_df))

output_downloaded_filename = 'intermediate outputs/urls_complete.csv'
temp_df = pd.read_csv(output_downloaded_filename, low_memory=False, names = ["id", "doc_url"])
print(temp_df.head(100))

print(list(temp_df))

urls_to_download_df.at[j,'pdf_download'] = 1

# Append to existing output
    urls_to_download_df.to_csv(merged_output_filename, index=True)
