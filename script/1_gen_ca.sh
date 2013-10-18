#!/bin/bash -x

# openssl genrsa -des3 -out ca.key 4096
# openssl req -new -x509 -days 3650 -key ca.key -out ca.crt

openssl req -new -x509 -days 3650 -newkey rsa:4096 -out ca.crt -keyout ca.key
