This folder contains a tileindex for DOPs (R-G-B-NIR, 20 cm, TIFF format) of Sachsen. It was created by using a python script.

Tile index:
- `DOP20_tileindex_SN.gpkg.gz`
- contains one polygon for every DOP
- download URL for each polygon is stored as attribute

Download script:
- `DOP20_tileindex_SN.py`
- extracts DOP download URLs using `selenium`
- creates tile index based on the DOP names in download URLs using `gdal`

License:
- `license.txt`
- data can be used citing the "Datenlizent Deutschland - Namensnennung - Version 2.0"
- see file for complete license

Links:
- [metadate, license](https://geomis.sachsen.de/geomis-client/?lang=de#/datasets/iso/52749cf1-027a-400e-8424-1cd3feef1108)
- [download data](https://www.geodaten.sachsen.de/batch-download-4719.html)
- [tile index download](https://github.com/mundialis/tile-indices/raw/main/DOP/SN/DOP20_tileindex_SN.gpkg.gz)
