payload_$(SYSTEM)_$(ARCH): 
	$(CLANG) $(CLANG_FLAGS) $(PAYLOAD_FLAGS) src/$(SYSTEM)/$(ARCH)/payload.s \
	-D IP_ADDRESS=$(shell $(PYTHON3) scripts/mishell-ip2hex.py $(IP) --show-ip --endianness=$(ENDIANNESS)) \
	-D IP_OFFSET=$(shell $(PYTHON3) scripts/mishell-ip2hex.py $(IP) --show-offset --endianness=$(ENDIANNESS)) \
	-D PORT=$(shell $(PYTHON3) scripts/mishell-port2hex.py $(PORT) --endianness=$(ENDIANNESS)) \
	-D $(shell [[ $(ENDIANNESS) == 1234 ]] && echo "LITTLE_ENDIAN" || echo "BIG_ENDIAN") \
	-o $@

payload_$(SYSTEM)_$(ARCH).bin: payload_$(SYSTEM)_$(ARCH)
	$(OBJCOPY) $(OBJCOPY_FLAGS) -O binary -j .text $^ $@

build: payload_$(SYSTEM)_$(ARCH).bin

echo:
	@echo "CLANG=$(CLANG)"
	@echo "CLANG_FLAGS=$(CLANG_FLAGS)"
	@echo "OBJCOPY=$(OBJCOPY)"
	@echo "OBJCOPY_FLAGS=$(OBJCOPY_FLAGS)"
	@echo "HOSTARCH=$(HOSTARCH)"
	@echo "PREFIX=$(PREFIX)"
	@echo "VERSION=$(VERSION)"
	@echo "PYTHON3=$(PYTHON3)"
	@echo "IP=$(IP)"
	@echo "PORT=$(PORT)"
	@echo "ARCH=$(ARCH)"
	@echo "SYSTEM=$(SYSTEM)"
	@echo "ENDIANNESS=$(ENDIANNESS)"
