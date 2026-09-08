This folder contains a tileindex for DOP tiles of Schleswig-Holstein. It was downloaded and converted to GPKG format using a python script.

Tileindex:
- `SH_DOP_tindex_proj.gpkg.gz`
- contains one polygon for each tile
- download links of the GeoTIFFs are stored as attribute ("location")

Download script:
- `SH_DOP_tindex.py`
- downloads tileindex (GeoJSON) from [GDI-SH](https://geodaten.schleswig-holstein.de/gaialight-sh/_apps/dladownload/dl-dop20.html)
- renames attribute "link_data" (containing the download URL) to "location"
- converts modified GeoJSON tileindex into GPKG format

Metadata:
- [metadata](https://www.schleswig-holstein.de/DE/landesregierung/ministerien-behoerden/LVERMGEOSH/Service/serviceGeobasisdaten/geodatenService_Geobasisdaten_DOP_digital)

Links:
- [license](https://geodaten.schleswig-holstein.de/gaialight-sh/_apps/dladownload/lizenz.html)
