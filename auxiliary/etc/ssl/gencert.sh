#!/bin/sh

openssl req -new -x509 -days 1095 -out xmlrpcd.cert.pem -key xmlrpcd.key.pem \
  -subj "/CN=$(hostname)"
