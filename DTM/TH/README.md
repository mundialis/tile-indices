This folder contains a tileindex for a DTM (DTM1 with size 1000 x 1000 m) of Thüringen. It was created by using a python script.

Tile index:
- `th_dtm_tindex_proj.gpkg.gz`
- contains one poylgon for every tile
- download URL for each poylgon is stored in attribute "location"

Download script:
- `TH_DTM_tindex.py`
- extracts UTM coordinates out of filenames
- based on the southwest corner it calculates the tile extents

Metadata:
- data can be used by citing "©GDI-TH CC BY 4.0", [Creative Commons Namensnennung 4.0 International](https://creativecommons.org/licenses/by/4.0/deed.de), [GDI-TH](https://geoportal.thueringen.de/gdi-th/download-offene-geodaten/download-hoehendaten)"

TH:

Links:
- [metadata, license, ...](https://geoportal.thueringen.de/gdi-th/download-offene-geodaten/download-hoehendaten)
