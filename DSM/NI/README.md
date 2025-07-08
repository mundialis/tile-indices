This folder contains a tileindex for DSM tiles (1000x1000 m) of Niedersachsen. It was downloaded and converted to GPKG format using a python script.

Tileindex:
- `NI_DSM_tindex_proj.gpkg.gz`
- contains one polygon for each tile
- download links of the GeoTIFFs are stored as attribute ("location")

Download script:
- `NI_DSM_tindex.py`
- downloads tileindex (GeoJSON) from [OpenGeoData.NI](https://ni-lgln-opengeodata.hub.arcgis.com/apps/lgln-opengeodata::digitales-oberfl%C3%A4chenmodell-dom1/about)
- removes not needed attributes and creates "location" attribute
- converts modified GeoJSON tileindex into GPKG format

Metadata:
- [metadata](https://ni-harvest-prod.geocat.live/catalogue/srv/ger/catalog.search#/metadata/a2226adb-bfa3-4309-a3e4-b17fcac064e0)

Links:
- [license](https://www.lgln.niedersachsen.de/startseite/wir_uber_uns_amp_organisation/allgemeine_geschafts_und_nutzungsbedingungen_agnb/allgemeine-geschafts-und-nutzungsbedingungen-agnb-97401.html)
