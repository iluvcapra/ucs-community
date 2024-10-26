# ucsxls2json.py 
# (c) 2024 Jamie Hardt
#
# This tool takes the "Full Translations" xlsx file and converts it into a
# series of json files, one for each language in the table.
#
# This script is a part of the `ucs-community` project, a LICENSE file outling
# your rights should be included in its distribution. For more information see 
# the project website on github: https://github.com/iluvcapra/ucs-community

import pandas as pd
import json
from typing import Dict
import os

# this key is added to ever category entry created in the output files
UCS_VERSION = "8.2.1"

# This is the file to pull descriptions from
EXCEL_FILE = 'UCS v8.2.1 Full Translations.xlsx'

data = pd.read_excel(EXCEL_FILE)

# Create a table of all languages that maps language-column pairs to their
# corresponding index in the xlsx

# The English column headers aren't formatted like the other languages so we
# just have to special-case them
langs: Dict[str,Dict[int,str]] = {'en': {0: 'Category', 1: 'SubCategory', 2:
                                         'CatID', 3:'CatShort',
                                         4:'Explanations', 5: 'Synonyms'}}

# step through each column
for i, (col_index, col_data) in enumerate(data.T.iterrows()):

    # the data is transposed, so indexing into col_data steps down in rows,
    # row[1] is where all the headers are.
    components = col_data[1].split("_")
    
    if len(components) == 2:
        # If this is true, we are in a translation column
        if components[0] == 'Category':
            langs[components[1]] = dict()
    
        langs[components[1]][i] = components[0]

os.makedirs("ucs_json", exist_ok=True)

# Pull the rows into a list
# skip the first three rows of the data, it's just header material
rows = list(data.iterrows())[3:]

# for each language

for lang in langs:
    # construct a schedule for the language
    schedule = []

    # for each row
    for (_, row) in rows:

        # create a dict for the category on this row
        category = {'version':UCS_VERSION}
        for col_index in langs[lang]:
            key_name = langs[lang][col_index]
            category[key_name] = row.iloc[col_index]
        
        schedule.append(category)

    # and dump it to json
    with open(f"ucs_json/{lang}.json", "w") as fp:
        json.dump(schedule, indent=True, fp=fp)
