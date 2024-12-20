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

import re
import json
import os
from typing import Dict, List

# this key is added to ever category entry created in the output files
UCS_VERSION = "8.2.1"

# This is the file to pull descriptions from
EXCEL_FILE = 'UCS v8.2.1 Full Translations.xlsx'

# Output directory, where all the output files will be written 
OUTPUT_DIR = 'json'

data = pd.read_excel(EXCEL_FILE)

# Create a table of all languages that maps language-column pairs to their
# corresponding index in the xlsx

# The English column headers aren't formatted like the other languages so we
# just have to special-case them
langs: Dict[str,Dict[int,str | List[str]]] = {'en': {0: 'Category', 1:
                                                     'SubCategory', 2: 'CatID',
                                                     3:'CatShort',
                                                     4:'Explanations', 5:
                                                     'Synonyms'}}

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

os.makedirs(OUTPUT_DIR, exist_ok=True)

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
        category: Dict[str, str | List[str]] = {'version':UCS_VERSION}
        for col_index in langs[lang]:
            key_name = str(langs[lang][col_index])
            category[key_name] = str(row.iloc[col_index])
            # Save the English CatID so this can be cross-referenced
            category['CatID'] = row.iloc[2]
            
            if key_name == 'Synonyms':
                # synonyms are stored in the spreadsheet as CSV, we should 
                # normalize this. 
                syns_raw = category['Synonyms']
                assert type(syns_raw) == str, \
                        f"Synonym list (lang: {lang}, {category['CatID']}) was not readable"
                split_pattern = r',\s*'
                if lang in ['zh','ar','kr','ja','tw']:
                    split_pattern = r'\W+'
                syn_list = re.split(split_pattern, syns_raw)
                category['Synonyms'] = [s.lower() for s in syn_list]

                # if the sub-category name is not in the synonym list, include it
                # if category['SubCategory'].lower() not in category['Synonyms']:
                    # category['Synonyms'].append(category['SubCategory'].lower())
                
                if lang == 'en':
                    for i, syn in enumerate(category['Synonyms']):
                        if syn == "a":
                            del category['Synonyms'][i]
        
        schedule.append(category)

    # and dump it to json
    with open(f"{OUTPUT_DIR}/{lang}.json", "w") as fp:
        json.dump(schedule, indent=True, fp=fp)
