"""
This script downloads the data and extracts it
"""

import os
import gzip
import shutil
import wget

print("Initializing variables")

PROJECT_PATH = os.getcwd()
IMDB_URL = "https://datasets.imdbws.com"
OUTPUT = "datasets"

IMDB_FILES = [
    "title.basics.tsv.gz",
    "title.principals.tsv.gz",
    "title.ratings.tsv.gz",
    "name.basics.tsv.gz",
]

if os.path.exists(os.path.join(PROJECT_PATH, OUTPUT)):
    shutil.rmtree(os.path.join(PROJECT_PATH, OUTPUT))
    os.mkdir(os.path.join(PROJECT_PATH, OUTPUT))
else:
    os.mkdir(os.path.join(PROJECT_PATH, OUTPUT))

print("Starting to get the data")

for file in IMDB_FILES:
    print(f"Processing: {file}")
    url = f"{IMDB_URL}/{file}"
    file_comp_out = os.path.join(PROJECT_PATH, OUTPUT, file)
    file_out = os.path.join(PROJECT_PATH, OUTPUT, file.replace(".gz", ""))

    # download file
    wget.download(url, out=file_comp_out)

    # extract file
    with gzip.open(file_comp_out, 'rb') as f_in:
        with open(file_out, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    print(f"\nextracted: {file}")

    # remove compressed file
    os.remove(file_comp_out)