This folder contains a tileindex for a DSM ("DOM") of Thüringen. It was created by using a bash shell script.

Tile index:
- `TH_DOM_tileindex_proj.gpkg.gz`
- contains one poylgon for every DSM
- download URL for each poylgon is stored as attribute

Generate Tile_index with csv file:

- the .csv file with download links of every tile had to be created manually. The download links were retrieved via an atom feed, published here: https://www.geoportal-th.de/de-de/Downloadbereiche/Download-Offene-Geodaten-Th%C3%BCringen/Download-H%C3%B6hendaten

- as the listed zip files cannot be recognized as a supported file format by GDAL ("error 4"), the respective xyz files in the zip folders must be specified.
Accordingly, the csv list was manually changed to e.g: `/vsizip/vsicurl/https://geoportal.geoportal-th.de/hoehendaten/DOM/dom_2014-2019/dom1_561_5610_1_th_2014-2019.zip/dom1_561_5610_1_th_2014-2019.xyz`.

Furthermore, defective tiles, that were lying outside the federal state were excluded.

- based on the output csv, a tileindex.gpkg can be generated by running: `gdaltindex -f GPKG TH_DOM_tileindex.gpkg --optfile TH_dom_list.csv`

License:
- `license.txt`
- data can be used citing the „Datenlizenz Deutschland - Namensnennung - Version 2.0“
- see file for complete license

Links:
- [metadata, license, ...](https://www.geoportal-th.de/de-de/Downloadbereiche/Download-Offene-Geodaten-Th%C3%BCringen/Download-H%C3%B6hendaten)
- [download data](https://www.geoportal-th.de/de-de/Downloadbereiche/Download-Offene-Geodaten-Th%C3%BCringen/Download-H%C3%B6hendaten)
TH:

# Thüringen (TH) Tile index of Digital Surface Model from Brandenburg Geobasis data

* Geoportal data: image based Digital Surface Model, 1m resolution,  EPSG:25832
* [Scripts](https://github.com/mundialis/tile-indices/tree/main/DSM/TH) to create the tile index
* Download link: https://github.com/mundialis/tile-indices/blob/main/DSM/TH/TH_DOM_tileindex.gpkg.gz
