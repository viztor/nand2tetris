// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input. 
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel. When no key is pressed, the
// program clears the screen, i.e. writes "white" in every pixel.

// Put your code here.

//INIT
	@color
	M=0

(LOOP)
	//init

	@8192
	D=A
	@i
	M=D

	@SCREEN
	D=A
	@screen
	M=D

	//keyboardDetection
	@KBD
	D=M

	@NOTPRESSED
	D;JEQ

	@color
	M=-1
	@RENDER
	0;JMP

(NOTPRESSED)
	@color
	M=0

(RENDER)
	@color
	D=M
	@screen
	A=M
	M=D
	@screen
	M=M+1

	//cond jmp
	@i
	D=M
	@i
	M=M-1
	@i
	D=M
	@RENDER
	D;JGT

//back to square one
	@LOOP
	0;JMP
