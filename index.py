# # # # # #
# # # # # #
# # # # # #
# #  A_setup
# # # # # #
# # # # # #
# # # # # #

python3 A_setup/01_get_company_numbers.py
python3 A_setup/02_select_subset_of_cns.py

# # # # # #
# # # # # #
# # # # # #
# #  B_get_metadata
# # # # # #
# # # # # #
# # # # # #

python3 B_get_metadata/03_get_doc_metadata.py


# # # # # #
# # # # # #
# # # # # #
# #  C_get_pdfs
# # # # # #
# # # # # #
# # # # # #

python3 C_get_pdfs/04_prep_metadata_for_pdf_api.py
python3 C_get_pdfs/05_download_pdfs.py

# # # # # #
# # # # # #
# # # # # #
# #  D_convert_to_text
# # # # # #
# # # # # #
# # # # # #

python3 D_convert_to_text/06_convert_pdfs_to_text.py

# # # # # #
# # # # # #
# # # # # #
# #  E_analyse_text
# # # # # #
# # # # # #
# # # # # #

python3 E_analyse_text/07_convert_text_to_structured_data.py

# # # # # #
# # # # # #
# # # # # #
# #  _tests
# # # # # #
# # # # # #
# # # # # #

python3 _tests/summary_stats.py
python3 _tests/test_01_check_new_output.py
python3 _tests/test_02_check_url_download_output.py
python3 _tests/test_03_generic_csv_test.py
python3 _tests/test_04_moving_pdfs.py
python3 _tests/test_05_take_a_look_co_numbs.py
python3 _tests/test_06_exploring_co_numbs_with_urls.py
