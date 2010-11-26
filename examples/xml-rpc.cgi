#!/usr/bin/perl

use warnings;
use strict;

use Frontier::RPC2;
use CGI qw/:standard/;

#-----------------------------------------------------------------------------

my $methods = "/srv/xmlrpc/methods/*/*.pm";

#-----------------------------------------------------------------------------
# prepare RPC mapping

my $public = {};
my $rpc_hash = {};

for my $file (glob $methods) {
  my $load = load_method($file);
  my $method_name = "$load->{schema}.$load->{method}";

  if (not exists $rpc_hash->{$method_name}) {
    $rpc_hash->{$method_name} = $load->{"proc"};
  }
}

#-----------------------------------------------------------------------------

my $rpc_server = new Frontier::RPC2();

my $req = new CGI();

if ($req->request_method ne 'POST') {
  print header(-status => "401 Forbidden");
  exit;
}

my $xml_resp = $rpc_server->serve($req->param('POSTDATA'), $rpc_hash);
print header(-status => "200 OK");
print $xml_resp;

#-----------------------------------------------------------------------------

sub load_method {
  my ($path) = @_;

  my $package = $path;
  $package =~ s/\.pm$//;

  ($package, my $method) = (split m[/+], $package)[-2, -1];

  if ("${package}::${method}" !~ /^[a-zA-Z0-9_]+::[a-zA-Z0-9_]+$/) {
    die "Path $path translates into incorrect package name: ${package}::${method}";
  }

  my $sub;
  eval "
    package rpcmethod::$package;
    require \$path;
    \$sub = \\&entry_point;
  ";
  die $@ if $@;

  return {
    schema => $package,
    method => $method,
    proc   => $sub,
  };
}

#-----------------------------------------------------------------------------
# vim:ft=perl
