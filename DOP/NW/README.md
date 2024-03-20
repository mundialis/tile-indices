# Nordrhein-Westfalen (NRW/NW) Tile index of Digitales Orthophoto from openNRW data

* openNRW data: Digitales Orthophoto, R-G-B-NIR, 10cm resolution, JP2000 format

Tile index:
- `DOP20_tileindex_BE_BB.gpkg.gz`
- contains one poylgon for every DOP
- download URL for each poylgon is stored as attribute ("location")

Create tileindex script:
- `DOP_tileindex_NW.py`
- extracts UTM coordinates out of DOP names
- based on the southwest corner it calculates the DOP extents
- requires a .csv file containing each download URL for all DOPs (no seperator, one URL per line) including the prefix "/vsicurl/"
- requires an output file path (.gpkg)
- depending on the URLs length the indexing in line 33 & 34 should be adjusted

Links
* Download link: https://github.com/mundialis/tile-indices/raw/main/DOP/NW/DOP10_tileindex_NW.gpkg.gz
* [metadata, license, ...](https://www.geoportal.nrw/?activetab=map#/datasets/iso/56fb584b-10cf-4009-a405-0bef06bb3e00)