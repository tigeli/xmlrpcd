#!/usr/bin/python

import xmlrpclib as xmlrpc

host = 'localhost'
port = 1638
(user, password) = ('nabla', 'nabla')

serv = xmlrpc.Server('https://%s:%s@%s:%d/' % (user, password, host, port))

print serv.authenticated_example.reverse(8, 20)

# vim:ft=python
