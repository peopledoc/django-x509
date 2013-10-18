#!/bin/bash -x

serial="0x`python -c "import uuid; print(str(uuid.uuid4()).replace('-', ''))"`"
openssl x509 -req -days 3650 -in client.csr -CA ca.crt -CAkey ca.key -set_serial "${serial}" -out client.crt

openssl x509 -subject -serial -noout -in client.crt
