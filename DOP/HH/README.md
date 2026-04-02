This folder contains a tileindex for DOPs (R-G-B-NIR, 20 cm, TIFF format) of Sachsen. It was created by using a python script.

Tile index:
- `DOP20_tileindex_HH.gpkg.gz`
- contains one polygon for every DOP
- download URL for each polygon is stored as attribute

Download script:
- `DOP20_tileindex_HH.py`
- extracts DOP download URLs using `selenium`
- creates tile index based on the DOP names in download URLs using `gdal`

License:
- `license.txt`
- data can be used citing the "Datenlizent Deutschland - Namensnennung - Version 2.0"
- see file for complete license

Links:
- [metadate, license](https://suche.transparenz.hamburg.de/api/3/action/package_show?id=luftbilder-hamburg-dop-zeitreihe-unbelaubt3)
- [download data](https://suche.transparenz.hamburg.de/dataset/luftbilder-hamburg-dop-zeitreihe-unbelaubt3)
- [tile index download](https://github.com/mundialis/tile-indices/raw/main/DOP/HH/DOP20_tileindex_HH.gpkg.gz)
