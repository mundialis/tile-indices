This folder contains a tileindex for DSM tiles (in this case DOM1 with size of 1000 x 1000 m) of Bremen and Bremerhaven. It was created by using a python script.

Tile index:
- `hb_dom1_tindex_proj.gpkg.gz`
- contains one poylgon for every tile
- filenames (from the [Bremen](https://gdi2.geo.bremen.de/inspire/download/DOM/data/Gitternetz_DOM1_2017_HB_ASCII_XYZ.zip) and [Bremerhaven](https://gdi2.geo.bremen.de/inspire/download/DOM/data/Gitternetz_DOM1_2015_BHV_ASCII_XYZ.zip) ZIP)
for each poylgon are stored as attribute "location"

Download script:
- `HB_DSM_tindex.py`
- extracts UTM coordinates out of filenames
- based on the southwest corner it calculates the tile extents

Metadata:
- data can be used citing the "Landesamt GeoInformation Bremen, [Creative Commons Namensnennung 4.0 International](https://creativecommons.org/licenses/by/4.0/deed.de), [DOM1](https://metaver.de/trefferanzeige?docuuid=5FDCE552-8111-46D3-9B13-A27A84EC1447&q=bremen%20dom1)"

Links:
- [metadata, license, ...](https://metaver.de/trefferanzeige?docuuid=5FDCE552-8111-46D3-9B13-A27A84EC1447&q=bremen%20dom1)
- [direct download Bremen](https://gdi2.geo.bremen.de/inspire/download/DOM/data/Gitternetz_DOM1_2017_HB_ASCII_XYZ.zip)
- [direct download Bremerhaven](https://gdi2.geo.bremen.de/inspire/download/DOM/data/Gitternetz_DOM1_2015_BHV_ASCII_XYZ.zip)
