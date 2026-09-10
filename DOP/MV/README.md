This folder contains a tileindex for DTM tiles (in this case DGM1 with size of 2000 x 2000 m) of Mecklenburg-Vorpommern. It was created by using a python script.

Tile index:
- `mv_dtm_tindex_proj.gpkg.gz`
- contains one poylgon for every tile
- download links of the GeoTIFFs are stored as attribute "location"

Download script:
- `MV_DTM_tindex.py`
- extracts UTM coordinates out of filenames
- based on the southwest corner it calculates the tile extents

Metadata:
- data can be used by citing "©GeoBasis-DE/MV/CC BY 4.0", [Creative Commons Namensnennung 4.0 International](https://creativecommons.org/licenses/by/4.0/deed.de), [LAiV M-V DGM1](https://laiv.geodaten-mv.de/afgvk/Geotopographie/Download?produkt=DGM1)"

Links:
- [metadata, license, ...](https://www.laiv-mv.de/Geoinformation/Geobasisdaten/Gelaendemodelle/)
