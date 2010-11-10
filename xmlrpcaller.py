#!/usr/bin/python

# server - RPC server address
# port   - RPC server port
# creds  - tuple of (username, password); give None if no HTTP-AUTH desired
# method - method name (most probably: package.function)
# args   - method arguments
def xml_rpcall(server, port, creds, method, *args):
  import xmlrpclib as xmlrpc
  import httplib as http
  import base64

  headers = { "Content-Type": "text/xml" }
  if creds != None:
    headers["Authorization"] = "Basic %s" % (base64.b64encode('%s:%s' % creds),)
  body = xmlrpc.dumps(args, methodname = method)

  server = http.HTTPSConnection(server, port)
  server.request("POST", "/", body, headers)
  resp = server.getresponse()
  if resp.status >= 400:
    raise xmlrpc.Fault("HTTP error %d (%s)" % (resp.status, resp.reason))
  xml_resp = resp.read()
  return xmlrpc.loads(xml_resp)[0][0]

# 'authenticated_example.reverse'
# 'public_example.sumAndDifference'

print xml_rpcall(
  'localhost', 1638, ('nabla', 'nabla'),
  'authenticated_example.reverse', 8, 20
)

# vim:ft=python
