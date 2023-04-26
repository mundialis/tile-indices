This folder contains a tileindex for DOPs (R-G-B-NIR, 20 cm, TIFF format) of Berlin and Brandenburg. It was created by using a python script.

Tile index:
- `DOP20_tileindex_BE_BB.gpkg.gz`
- contains one poylgon for every DOP
- download URL for each poylgon is stored as attribute

Download script:
- `DOP_tileindex_BE_BB.py`
- extracts UTM coordinates out of DOP names
- based on the southwest corner it calculates the DOP extents
- requires a .csv file containing each download URL for all DOPs (no seperator, one URL per line) including the prefix "/vsizip/vsicurl/"
- requires an output file path (.gpkg)
- depending on the URLs length the indexing in line 33 & 34 should be adjusted

License:
- `license.txt`
- data can be used citing the „Datenlizenz Deutschland - Namensnennung - Version 2.0“
- see file for complete license

Links:
- [metadata, license, ...](https://geoportal.brandenburg.de/detailansichtdienst/render?url=https://geoportal.brandenburg.de/gs-json/xml?fileid=253b7d3d-6b42-47dc-b127-682de078b7ae)
- [download data](https://data.geobasis-bb.de/geobasis/daten/dop/)
