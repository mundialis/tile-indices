This folder contains a tileindex for DOP tiles of Niedersachsen. It was downloaded and converted to GPKG format using a python script.

Tileindex:
- `NI_DOP_tindex_proj.gpkg.gz`
- contains one polygon for each tile
- download links of the GeoTIFFs are stored as attribute ("location")

Download script:
- `NI_DOP_tileindex.py`
- downloads tileindex (GeoJSON) from [OpenGeoData.NI](https://ni-lgln-opengeodata.hub.arcgis.com/apps/lgln-opengeodata::digitales-orthophoto-dop/about)
- filters overlapping tiles and only keeps latest ones
- removes not needed attributes and creates "location" attribute
- converts modified GeoJSON tileindex into GPKG format

Metadata:
- [metadata](https://ni-harvest-prod.geocat.live/catalogue/srv/ger/catalog.search#/metadata/87890b7a-5a8a-4100-8a1e-78ced663a5d4)

Links:
- [license](https://www.lgln.niedersachsen.de/startseite/wir_uber_uns_amp_organisation/allgemeine_geschafts_und_nutzungsbedingungen_agnb/allgemeine-geschafts-und-nutzungsbedingungen-agnb-97401.html)
