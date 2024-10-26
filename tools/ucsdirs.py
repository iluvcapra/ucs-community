# ucsdirs.py 
# (c) 2024 Jamie Hardt
#
# This tool creates a directory tree of UCS category and sub-categories
# according to the selected language schedule.
#
# This script is a part of the `ucs-community` project, a LICENSE file outling
# your rights should be included in its distribution. For more information see 
# the project website on github: https://github.com/iluvcapra/ucs-community

import os
import sys
import json

# The path to the UCS schedule json
SCHEDULE_JSON=sys.argv[1]

# The path to create the directory tree in
OUTPUT_PATH=sys.argv[2]

schedule = []

with open(SCHEDULE_JSON, "r") as fp:
    entries = json.load(fp=fp)
    schedule.extend(entries)

for cat in schedule:
    path = os.path.join(OUTPUT_PATH, cat['Category'], 
                        f"{cat['Category']} - {cat['SubCategory']}")
    os.makedirs(path, exist_ok=True)

