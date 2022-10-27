# The default test target, payloads either include this or define one for themselves

test_$(SYSTEM)_$(ARCH): payload_$(SYSTEM)_$(ARCH).bin
	cp $^ payload
	xxd -i payload test/payload.h
	$(CLANG) test/test.c $(CLANG_FLAGS) -o $@
	rm -f test/payload.h payload

test: test_$(SYSTEM)_$(ARCH)
	@echo "This is a dangerous command to run,"
	@echo "it may really open a shell for someone else to your pc"
	-./test_$(SYSTEM)_$(ARCH)

.PHONY: test
