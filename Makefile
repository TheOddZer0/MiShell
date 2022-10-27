# Copyright (c) 2022 TheOddZer0
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
# of the Software, and to permit persons to whom the Software is furnished to do
# so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

PYTHON3    :=python3
IP         :=127.0.0.1
PORT       :=4444
SHELL      :=/bin/bash
HOSTARCH   :=$(shell uname -m | sed s/i[3456789]86/i386/)
SYSTEM     :=$(shell uname -s | awk '{print tolower($$0)}')

ifeq ($(ARCH),)
ARCH       =$(HOSTARCH)
endif

# To be honest, passing ARCH=amd64 is sometimes easier. Let's also support that.
ifeq ($(ARCH),amd64)
ARCH=x86_64
endif

all: build

include src/$(SYSTEM)/$(ARCH)/build.mak

distclean: clean

.PHONY: all distclean 
