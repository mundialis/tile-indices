This folder contains a tileindex for DSM tiles (DSM1 with size 2000 x 2000 m) of Baden-Württemberg. It was created by using a python script.

Tile index:
- `BW_DSM_tindex_proj.gpkg.gz`
- contains one polygon for every tile
- download URL for each polygon is stored in attribute "location"

Download script:
- `BW_DSM_tindex.py`
- extracts UTM coordinates out of filenames
- based on the southwest corner it calculates the tile extents

Metadata:
- data can be used by citing "Datenquelle LGL, https://www.lgl-bw.de, [dl-de/by-2-0](https://www.govdata.de/dl-de/by-2-0)", [DSM1](https://opengeodata.lgl-bw.de/#/(sidenav:product/dom1))

Links:
- [metadata, license, ...](https://www.lgl-bw.de/Produkte/Open-Data/)
