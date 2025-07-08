This folder contains a tileindex for DTM tiles (1000x1000 m) of Niedersachsen. It was downloaded and converted to GPKG format using a python script.

Tileindex:
- `NI_DTM_tindex_proj.gpkg.gz`
- contains one polygon for each tile
- download links of the GeoTIFFs are stored as attribute ("location")

Download script:
- `NI_DTM_tileindex.py`
- downloads tileindex (GeoJSON) from [OpenGeoData.NI](https://ni-lgln-opengeodata.hub.arcgis.com/apps/lgln-opengeodata::digitales-gel%C3%A4ndemodell-dgm1/about)
- removes not needed attributes and creates "location" attribute
- converts modified GeoJSON tileindex into GPKG format

Metadata:
- [metadata](https://ni-harvest-prod.geocat.live/catalogue/srv/ger/catalog.search#/metadata/740e33da-3310-4173-bae1-d30c31124b3a)

Links:
- [license](https://www.lgln.niedersachsen.de/startseite/wir_uber_uns_amp_organisation/allgemeine_geschafts_und_nutzungsbedingungen_agnb/allgemeine-geschafts-und-nutzungsbedingungen-agnb-97401.html)
