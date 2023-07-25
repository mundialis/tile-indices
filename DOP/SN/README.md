This folder contains a tileindex for DOPs (R-G-B-NIR, 20 cm, TIFF format) of Sachsen. It was created by using a python script.

Tile index:
- `DOP20_tileindex_SN.gpkg.gz`
- contains one polygon for every DOP
- download URL for each polygon is stored as attribute

Download script:
- `DOP20_tileindex_SN.py`
- it is the same script as for creating the tile index of BB and BE (see `../BE_BB/DOP20_tileindex_BE_BB.py`) including small modifications (tile size)
- .csv file containing needed download URLs: `SN_DOP20_URLs.csv`

License:
- `license.txt`
- data can be used citing the "Datenlizent Deutschland - Namensnennung - Version 2.0"
- see file for complete license

Links:
- [metadate, license](https://geomis.sachsen.de/geomis-client/?lang=de#/datasets/iso/52749cf1-027a-400e-8424-1cd3feef1108)
- [download data](https://www.geodaten.sachsen.de/batch-download-4719.html)
