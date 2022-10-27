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
import sys

parser = argparse.ArgumentParser(
    description="Encode integer port into hex form, taking care of endianness"
)


def _hex(num: int):
    result = hex(num)[2:]
    if len(result) % 2 != 0:
        result = "0" + result
    return result


def _reorder(value: str, endianness: str):
    if endianness in ("little", "l", "1234"):
        # Get chunks of two from the result
        chunks = [value[i:i+2] for i in range(0, len(value), 2)]
        chunks.reverse()
        return "".join(chunks)
    return value


def main(argv=None):
    parser.add_argument("port", type=int,
                        help="The port to convert to hex (while taking care of the endianness)")
    parser.add_argument("--endianness", "-e", choices=["big", "b", "little", "l", "1234", "4321"],
                        help="Define the endianness, big or little (also b and l)", default="l")
    ns = parser.parse_args(argv)
    if ns.port == -1:
        try:
            ns.port = int(input())
        except ValueError:
            ns.port = -1
    # 65535 is the maximum for an `unsigned short`
    # so the length of the result will be two bytes
    if ns.port not in range(65535 + 1):
        print(f"Invalid port '{ns.port}'", file=sys.stderr)
        sys.exit(1)
    print(f"0x{_reorder(_hex(ns.port), ns.endianness)}")


if __name__ == "__main__":
    main()
