.PHONY: run call

CONFIG  = etc/xmlrpcd.conf
LOGCONF = etc/logging.conf
PIDFILE = run/xmlrpcd.pid

debug = 0

run:
ifeq ($(debug),1)
	../xmlrpcd --config $(CONFIG) -l4p $(LOGCONF) -p $(PIDFILE) -X
else
	../xmlrpcd --config $(CONFIG) -l4p $(LOGCONF) -p $$PWD/$(PIDFILE)
endif

kill:
	if [ -e $(PIDFILE) ]; then kill -TERM `cat $(PIDFILE)`; fi
	rm -f $(PIDFILE)

call:
	../xmlrpcaller --config etc/caller.conf --skip-ca --host localhost $(method) $(args)
