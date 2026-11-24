This folder contains a tileindex for DTM tiles (in this case DGM1 with size of 1000 x 1000 m) of Saarland. It was created by using a python script.

Tile index:
- `SL_DTM_tindex_proj.gpkg.gz`
- contains one polygon for every tile
- download links of the GeoTIFFs are stored as attribute "location"

Download script:
- `SL_DTM_tindex.py`
- extracts UTM coordinates out of filenames
- based on the southwest corner it calculates the tile extents

Metadata:
- data can be used by citing "© GeoBasis DE/LVGL-SL", [Datenlizenz Deutschland Namensnennung 2.0](https://www.govdata.de/dl-de/by-2-0), [GeoPortal Saarland](https://geoportal.saarland.de/)"

Links:
- [metadata, license, ...](https://metaver.de/trefferanzeige?docuuid=d73285be-e3a1-46ef-9562-88883dc0f9c0&plugid=/ingrid-group:iplug-csw-dsc-gdi-sl&docid=0M9bG30B-Xhv7YYsyVGu)
