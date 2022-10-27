# MiShell

MiShell is a multi-platform, multi-architecture project which offers super super small reverse shell payloads great for injection in buffer overflow vulnerabilities, written in assembly with a lot of tools written in python3.

## Info about this project

1. Completely Null-free even if your IP has zero's in it.

2. Supports your 32-bit and 64-bit home PC! (other architectures will be added).

3. With the supplied generator, you don't even need to compile it!

4. Easy installation.

5. No dependencies.

6. We plan on adding a lot more architectures and operating systems.

Well, If you are interested in having this shell code, Why waiting??

Just install it, It will be real easy!

## Method One

I know that you like getting a single line command which you can just copy and execute.
So here you go (wget):

```shell
wget https://github.com/TheOddZer0/MiShell/raw/main/scripts/mishell-gen.py
```

If you have curl, That does the job, too:

```shell
curl https://github.com/TheOddZer0/MiShell/raw/main/scripts/mishell-gen.py -o mishell-gen.py
```

The generator script doesn't depend on the rest of this repository and can go anywhere python3 can go. Which means your Termux, Linux, Windows, MacOS or BSD is capable of generating the payload.

Call the generator with ip and port to get the result in encoded form, pass `--raw` to get raw bytes. (See `--help` for yourself)

## Method Two

### Configuring the attacker IP

Just pass `IP=<your_ip> PORT=<port>` to the make command to configure it.

### Build

Now, run `make build` to build it for your current architecture and platform.
You can pass `ARCH` to make to change the architecture, currently `i386` and `x86_64` are supported

## Contacting the author

You can always send an email to me. I'm available at `TheOddZer0@protonmail.com`.

## License

This project is licensed under the MIT License, see the [LICENSE](https://github.com/TheOddZer0/MiShell/blob/main/LICENSE) for more information.
