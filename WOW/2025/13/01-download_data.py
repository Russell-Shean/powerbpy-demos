'''
This script downloads the data from Github and
then extracts the individual datasets from the compressed archive file.
'''
# pylint: disable=line-too-long
# pylint: disable=import-error
# pylint: disable=invalid-name

import os
import tempfile
import requests
import py7zr

# step 1: obtain data from github --------------------------------------------------------------

# Define paths
DATASET_URL = "https://github.com/sql-bi/Contoso-Data-Generator-V2-Data/releases/download/ready-to-use-data/csv-10k.7z"
DATA_DESTINATION_DIR = "data"


# make sure the folder exists
os.makedirs(DATA_DESTINATION_DIR, exist_ok=True)

# download the zip file from the internet
response = requests.get(DATASET_URL, stream=True)
response.raise_for_status()

# write to file
with tempfile.NamedTemporaryFile(suffix=".7z", delete=False) as tmp_file:
    with open(tmp_file.name, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)



# extract the data
with py7zr.SevenZipFile(tmp_file.name, mode="r") as z:
    z.extractall(path=DATA_DESTINATION_DIR)
