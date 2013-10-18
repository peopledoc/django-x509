#!/bin/bash -x

# openssl genrsa -des3 -out client.key 4096
# openssl req -new -key client.key -out client.csr

openssl req -new -newkey rsa:4096 -out client.csr -keyout client.key
