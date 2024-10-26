# Universal Category System - Community Resources

## What is this?

This repository contains documentation and some developer resources for the 
[Universal Category System][ucs], a library classification system and file 
naming convention for sound effects recordings used widely in the motion
picture, television and videogame/interactive industries.

[ucs]: https://universalcategorysystem.com

## What's here?

Some items of interest are:

  - [JSON-formatted UCS Schedules](json/) of version **8.2.1** of the UCS in 
    all available languages.
    - The [tool](tools/ucsxls2json.py) used to make these JSON files from the
      original XLS file.
  - Transcriptions of core UCS documentation into ReStructuredText:
    - Tim Nielsen's original [*UCS File Naming Convention*][ucs_fns] document.
    - An unofficial [list of released UCS versions](docs/versions.rst).
  - A [link tree](docs/links.rst) to UCS resources.
  - Zipped [UCS Category-SubCategory directory trees](dirs) in all of the
    available languages.
    - The [directory-creation tool](tools/ucsdirs.py) that was used to create 
      these trees from the JSON UCS schedules.
 
 [ucs_fns]:docs/ucs_file_naming_convention.rst

## Who maintains this?

This repository is maintained by [Jamie Hardt][jh]. I'm a user of UCS but I 
don't otherwise have any formal affiliation with Tim Nielsen, Justin Drury or 
the UCS creators or website.

[jh]: https://github.com/iluvcapra
