#!/bin/bash -x

openssl req -new -newkey rsa:4096 -nodes -out server.csr -keyout server.key
