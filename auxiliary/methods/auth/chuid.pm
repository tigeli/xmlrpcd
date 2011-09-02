our $RPC_UID = "www-data";
our $RPC_GID = "www-data";
our $RPC_PARAMS = [qw[user address]];

sub entry_point {
  my ($user, $addr, @args) = @_;

  return {
    user => `id`,
    args => \@args,
    auth_user => $user,
    call_addr => $addr,
  };
}

1;
