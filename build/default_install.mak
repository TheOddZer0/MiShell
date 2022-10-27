PREFIX     :=/usr/local/
VERSION    :=1.0.0

$(PREFIX)/src/MiShell-$(VERSION):
	mkdir -p $@
	rm -rf $@/**
	cp -r ./** $@/
	make -C $@/ clean
	chmod +x $@/scripts/**
	cp $@/scripts/** $(PREFIX)/bin/

$(PREFIX)/bin/mishell-gen:
	./payload2generator.py > $@
	chmod +x $@

install: $(PREFIX)/src/MiShell-$(VERSION)

generator: $(PREFIX)/bin/mishell-gen

.PHONY: generator install
