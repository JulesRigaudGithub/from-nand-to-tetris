// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.

@24576
D=A
@n
M=D



@KBD
D=M
@CLEAN
D;JEQ



(FILL)
@SCREEN
D=A

@addr
M=D

(LOOP1)
@addr
A=M
M=-1
@addr
M=M+1
D=M
@n
A=M
D=A-D
@LOOP1
D;JGT

(SCAN1)
@KBD
D=M
@CLEAN
D;JEQ
@SCAN1
0;JMP

(CLEAN)
@SCREEN
D=A

@addr
M=D

(LOOP2)
@addr
A=M
M=0
@addr
M=M+1
D=M
@n
A=M
D=A-D
@LOOP2
D;JGT

(SCAN2)
@KBD
D=M
@FILL
D;JNE
@SCAN2
0;JMP






