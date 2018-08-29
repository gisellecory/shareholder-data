import shutil
import os

source = "pdfs_test/"
destination = "pdfs_used/"


folder = os.listdir(source)

for file in folder:
        shutil.move(source+file, destination)
        print("Moved " + str(file))
