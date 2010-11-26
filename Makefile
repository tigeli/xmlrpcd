DESTDIR =
PREFIX = /usr/local
DOCDIR = $(PREFIX)/share/doc/xmlrpcd
BINDIR = $(PREFIX)/bin
SBINDIR = $(PREFIX)/sbin
EXAMPLES = $(DOCDIR)/examples
SYSCONFDIR = $(PREFIX)/etc
STATEDIR = $(PREFIX)/var

.PHONY: all install clean

all: # empty
clean: # empty

install:
	mkdir -p $(DESTDIR)$(PREFIX)
	mkdir -p $(DESTDIR)$(DOCDIR)
	mkdir -p $(DESTDIR)$(EXAMPLES)
	mkdir -p $(DESTDIR)$(SYSCONFDIR)/xmlrpcd
	mkdir -p $(DESTDIR)$(BINDIR)
	mkdir -p $(DESTDIR)$(SBINDIR)
	mkdir -p $(DESTDIR)$(STATEDIR)/run/xmlrpcd
	mkdir -p $(DESTDIR)$(STATEDIR)/lib/xmlrpcd
	install -m 755 xmlrpcaller  $(DESTDIR)$(BINDIR)/xmlrpcaller
	install -m 755 xmlrpcd      $(DESTDIR)$(SBINDIR)/xmlrpcd
	cp -R          examples/procedures     $(DESTDIR)$(EXAMPLES)
	install -m 644 examples/xmlrpcaller.py $(DESTDIR)$(EXAMPLES)
	install -m 644 examples/xml-rpc.cgi    $(DESTDIR)$(EXAMPLES)
	install -m 644 examples/logging.conf.example     $(DESTDIR)$(SYSCONFDIR)/xmlrpcd
	install -m 644 examples/xmlrpcaller.conf.example $(DESTDIR)$(SYSCONFDIR)/xmlrpcd
	install -m 644 examples/xmlrpcd.conf.example     $(DESTDIR)$(SYSCONFDIR)/xmlrpcd

.PHONY: srpm

srpm: VERSION=$(shell awk '$$1 == "%define" && $$2 == "_version" {print $$3}' redhat/xmlrpcd.spec)
srpm:
	rm -rf rpm-build
	mkdir -p rpm-build/rpm/{BUILD,RPMS,SOURCES,SPECS,SRPMS}
	git archive --format=tar --prefix=xmlrpcd-$(VERSION)/ HEAD | gzip -9 > rpm-build/rpm/SOURCES/xmlrpcd-$(VERSION).tar.gz
	rpmbuild --define="%_usrsrc $$PWD/rpm-build" --define="%_topdir %{_usrsrc}/rpm" -bs redhat/xmlrpcd.spec
	mv rpm-build/rpm/SRPMS/xmlrpcd-*.src.rpm .
	rm -r rpm-build
