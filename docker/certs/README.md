# Additional CA Certificates

Some state servers do not send their intermediate certificate, so TLS
verification fails inside the Docker image. The missing intermediate
certificates are stored here and registered in the `Dockerfile` with
`update-ca-certificates`.

## d-trust-br-ca-1-20-1-2020.crt

- Used for: `geodaten.schleswig-holstein.de` (DTM and iDSM SH)
- Reason: server does not send its intermediate certificates. Without this file
  `curl` fails with Error 60 (unable to get local issuer certificate)
- Subject: C=DE, O=D-Trust GmbH, CN=D-TRUST BR CA 1-20-1 2020
- Issuer: C=DE, O=D-Trust GmbH, CN=D-TRUST BR Root CA 1 2020
- Valid until: 2035-02-11 (notAfter=Feb 11 09:44:59 2035 GMT)
- Source: http://www.d-trust.net/cgi-bin/D-TRUST_BR_CA_1-20-1_2020.crt
  (from the "CA Issuers" entry of the server certificate, converted to PEM)
- Check without local OpenSSL:

  ```bash
  docker run --rm -v "$PWD/docker/certs:/c" osgeo/grass-gis:current-alpine \
     sh -c "apk add -q openssl && openssl x509 -in /c/<file>.crt -noout -subject -issuer -enddate"
  ```

### Renew the certificate / get one for a new server
1. Get the host from the URL in tindex script and start a container:

   ```bash
   docker run --rm -it osgeo/grass-gis:current-alpine sh
   ```

   Then inside the container:

   ```bash
   apk add curl openssl
   HOST=geodaten.schleswig-holstein.de # replace with the host from the script
   ```

2. Check the certificate chain:

   ```bash
   openssl s_client -connect $HOST:443 -servername $HOST -showcerts </dev/null 2>/dev/null | grep -E "^ *[0-9] s:|verify"
   ```

   Only one certificate plus verify error 21 means that the intermediate
   certificate is missing
3. Read the issuer and the download address:

   ```bash
   openssl s_client -connect $HOST:443 -servername $HOST </dev/null 2>/dev/null | openssl x509 -noout -issuer -ext authorityInfoAccess
   ```

4. Download the certificate and convert it to PEM (with `-L`, otherwise the
   file might stay empty):

   ```bash
   curl -sSL -o inter.cer "<CA-Issuers-URI>"
   openssl x509 -inform DER -in inter.cer -out inter.crt || openssl x509 -in inter.cer -out inter.crt
   ```

5. Check it: `openssl x509 -in inter.crt -noout -subject -issuer -enddate`
6. Save it as `.crt` in `docker/certs/`. The `Dockerfile` registers it with
   `update-ca-certificates`

   Copy the file out of the running container from a second terminal
   (`docker ps` shows the Container ID):

   ```bash
   docker cp <container-id>:/grassdb/inter.crt docker/certs/<name>.crt
