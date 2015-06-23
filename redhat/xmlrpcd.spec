%define _version 1.0
%define _release 1
%define _packager Stanislaw Klekot <dozzie@jarowit.net>

Summary: xmlrpcd - XML-RPC over HTTPs daemon/client
Name: xmlrpcd
Version: %{_version}
Release: %{_release}
Group: System Environment/Daemons
License: GPL v2
Source0: xmlrpcd-%{_version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-root
# Authen::Simple::Passwd (htpasswd) and methods necessary for it to work
Requires: perl(Authen::Simple::Passwd)
Requires: perl(Class::Accessor), perl(Class::Data::Inheritable)
# Log::Dispatch and necessary Sys::Syslog version
Requires: perl(Log::Dispatch), perl(Sys::Syslog) >= 0.16
# xmlrpcaller uses set_ctx_defaults function, which was added in 1.14 version
Requires: perl(IO::Socket::SSL) >= 1.14
# on RHEL7 HTTPs support was extracted to a separate package
Requires: perl(LWP::Protocol::https)
BuildArch: noarch
Packager: %{_packager}
Prefix: %{_prefix}

%define useradd /usr/sbin/useradd
%define groupadd /usr/sbin/groupadd

%define xmlrpcd_user xmlrpcd
%define xmlrpcd_group xmlrpcd

%description
This is small XML-RPC server, that supports HTTPs and HTTP authentication. It
doesn't need any big HTTP server, such as Apache or lighttpd.

Main goal was to provide easy-to-setup RPC daemon, that supports X.509/SSL
(for traffic protection) and optional authentication.

%prep
rm -rf $RPM_BUILD_DIR/xmlrpcd-%{_version}
tar zxf %SOURCE0

%build
cd xmlrpcd-%{_version}
make OPTIMIZE="%{optflags}"

%install

cwd=${PWD}
cd xmlrpcd-%{_version}
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf "$RPM_BUILD_ROOT"
make install \
  PREFIX=%{_prefix} \
  SYSCONFDIR=%{_sysconfdir} \
  STATEDIR=%{_localstatedir} \
  DOCDIR=%{_defaultdocdir}/xmlrpcd-%{_version} \
  DESTDIR="$RPM_BUILD_ROOT"

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/init.d
install -m 755 redhat/xmlrpcd.init $RPM_BUILD_ROOT%{_sysconfdir}/init.d/xmlrpcd
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/log/xmlrpcd

# %clean
# no %clean section


%files
%{_bindir}/xmlrpcaller
%{_sbindir}/xmlrpcd
%{_defaultdocdir}/xmlrpcd-%{_version}
%{_mandir}/man1/xmlrpcaller.1.gz
%{_mandir}/man8/xmlrpcd.8.gz
%config(noreplace) %{_sysconfdir}/init.d/xmlrpcd
%config %{_sysconfdir}/xmlrpcd/*.example
%attr(-,   %{xmlrpcd_user}, %{xmlrpcd_group}) %dir %{_sysconfdir}/xmlrpcd
%attr(755, %{xmlrpcd_user}, %{xmlrpcd_group}) %dir %{_localstatedir}/lib/xmlrpcd
%attr(755, %{xmlrpcd_user}, %{xmlrpcd_group}) %dir %{_localstatedir}/log/xmlrpcd


%pre

HAVE_XMLRPCD=`getent group %{xmlrpcd_group}`
if [ -z "$HAVE_XMLRPCD" ]; then
  %{groupadd} -r %{xmlrpcd_group} > /dev/null 2>&1
  echo "The group %{xmlrpcd_group} has been added."
fi
HAVE_XMLRPCD=`getent passwd %{xmlrpcd_user}`
if [ -z "$HAVE_XMLRPCD" ]; then
  %{useradd} -r -c "XML-RPC Server Account" -d %{_localstatedir}/run/xmlrpcd -M -s /sbin/nologin -g %{xmlrpcd_group} %{xmlrpcd_user} > /dev/null 2>&1
  echo "The user %{xmlrpcd_user} has been added."
fi

%post
/sbin/chkconfig --add xmlrpcd
# don't start the server by default
/sbin/chkconfig xmlrpcd off
/etc/init.d/xmlrpcd condrestart

%preun
/sbin/chkconfig --del xmlrpcd

# %changelog
# no %changelog section
