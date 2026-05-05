This folder contains a tileindex for DTM tiles (in this case DGM1 with size of 1000 x 1000 m) of Bremen and Bremerhaven. It was created by using a python script.

Tile index:
- `hb_dgm1_tindex_proj.gpkg.gz`
- contains one poylgon for every tile
- filenames (from the [Bremen](https://gdi2.geo.bremen.de/inspire/download/DGM/data/Gitternetz_DGM1_2017_HB_ASCII_XYZ.zip) and [Bremerhaven](https://gdi2.geo.bremen.de/inspire/download/DGM/data/Gitternetz_DGM1_2015_BHV_ASCII_XYZ.zip) ZIP)
for each poylgon are stored as attribute "location"

Download script:
- `HB_DTM_tindex.py`
- extracts UTM coordinates out of filenames
- based on the southwest corner it calculates the tile extents

Metadata:
- data can be used citing the "Landesamt GeoInformation Bremen, [Creative Commons Namensnennung 4.0 International](https://creativecommons.org/licenses/by/4.0/deed.de), [DGM1](https://www.metaver.de/trefferanzeige?docuuid=2351ABA6-019D-4155-853F-76EEFC26CA52)"

Links:
- [metadata, license, ...](https://www.metaver.de/trefferanzeige?docuuid=2351ABA6-019D-4155-853F-76EEFC26CA52)
- [direct download Bremen](https://gdi2.geo.bremen.de/inspire/download/DGM/data/Gitternetz_DGM1_2017_HB_ASCII_XYZ.zip)
- [direct download Bremerhaven](https://gdi2.geo.bremen.de/inspire/download/DGM/data/Gitternetz_DGM1_2015_BHV_ASCII_XYZ.zip)
