#!/usr/bin/ruby

require 'xmlrpc/client'

host = 'localhost'
port = 1638
user = 'nabla'
password = 'nabla'

# we will need to force SSL engine not to validate server certificate (don't
# do this in production! always do validate certificates!)
class XMLRPC::Client
  attr_accessor :http
end

serv = XMLRPC::Client.new_from_hash({
  :host => host, :port => port,
  :user => user, :password => password,
  :use_ssl => true
})
serv.http.verify_mode = OpenSSL::SSL::VERIFY_NONE

puts serv.call('authenticated_example.reverse', 8, 20)

# vim:ft=ruby
