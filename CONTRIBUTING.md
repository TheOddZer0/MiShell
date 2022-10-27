Before anything, **Thanks for taking the time to contribute to this project.**

## How to contribute a payload

**To keep constant dependencies and build flow, Gnu Assembler is the ONLY assembler we will use.**

After you got your copy of the repository, check this [wikipedia page](https://wikipedia.org/wiki/uname) for possible output of `uname`.
If it's a linux payload, the folder is already created, just enter it and make a folder with the architecture name (use the table in wikipedia link above as
some architectures may get called a couple of things). Create a `build.mak` file to instruct the build system to how to build it, a template for it is:

```make
include data/default_build.pre.mak
LDFLAGS    +=<usually defines the output format, but add anything which is required>
ASFLAGS    +=<Usually --32 or --64 but you can also add other flags>
CFLAGS     +=<Usually -m32 or -m64 but you may also add other flags>
ENDIANNESS  =<1234 for little endian, 4321 for big endian>
include data/defaults.mak 
```

Which uses the defaults to supply the build system, now write your payload inside a file named `payload.s`
(we first pass this file to cpp so c-style compiler directives work). And it's done. Test it a few places before making a pull request!

## How to contribute a script

Again for keeping a constant work flow, scripts should be only in python. Try to support big and little endian (if it effects your script).
Test it out and do the pull request!

## My way of contribution is not listed here

Then you can tell us and we will write guidelines for your way of contribution. just create an issue!
