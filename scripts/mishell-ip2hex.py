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
"""
import sys
import argparse

parser = argparse.ArgumentParser(
    description="Encode an IP address, avoiding zero bytes",
)


def _hex(num: int):
    result = hex(num)[2:]
    if len(result) % 2 != 0:
        result = "0" + result
    return result


def _reorder_list(value: list, endianness: str):
    if endianness in ("little", "l", "1234"):
        # Get chunks of two from the result
        value.reverse()
        return value
    return value


def main(argv=None):
    parser.add_argument("ip", help="The IP to encode")
    parser.add_argument("--show-offset", "-o",
                        help="Show the offset", action="store_true", default=False)
    parser.add_argument("--show-ip", "-i", help="Show the result IP",
                        action="store_true", default=False)
    parser.add_argument("--endianness", "-e", choices=["big", "b", "little", "l", "1234", "4321"],
                        help="Define the endianness, big or little (also b and l)", default="l")
    ns = parser.parse_args(argv)
    ip = ns.ip.strip()
    if ip == "-":
        ip = input()
    hexed = "0x"
    offset = "0x"
    parts = ip.split(".")
    if len(parts) != 4:
        print("That is actually not a valid IP address", file=sys.stderr)
        sys.exit(1)
    _reorder_list(parts, ns.endianness)
    for part in parts:
        try:
            part = int(part)
        except:
            print(f"Invalid IP '{ip}'", file=sys.stderr)
            sys.exit(1)
        if part > 255 or part < 0:
            print(f"Invalid IP '{ip}'", file=sys.stderr)
            sys.exit(1)
        if part == 255:
            print("This method will not work on your IP", file=sys.stderr)
            sys.exit(1)
        _hexed = _hex(part + 1)
        if _hexed != "00":
            hexed += _hexed
            offset += "01"
        else:
            hexed += _hex(part + 2)
            offset += "02"
    if ns.show_offset:
        print(f"{offset}")
    if ns.show_ip:
        print(f"{hexed}")


if __name__ == "__main__":
    main()
