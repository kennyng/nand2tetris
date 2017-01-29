// This file is part of the materials accompanying the book 
// "The Elements of Computing Systems" by Nisan and Schocken, 
// MIT Press. Book site: www.idc.ac.il/tecs
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[3], respectively.)

	@R2
	M=0 	// mult=0
	@count
	M=0	// count=0
(LOOP)
	@count
	D=M	// D=count
	@R0
	D=D-M	// D=count-RAM[0]
	@END
	D;JGE	// If (count-RAM[0]) >= 0 goto END
	@R2
	D=M	// D=mult
	@R1
	D=D+M	// D=D+RAM[1]
	@R2
	M=D	// Store D into mult
	@count
	M=M+1	// count=count+1 (or count++)
	@LOOP
	0;JMP	// Goto LOOP
(END)
	@END
	0;JMP	// Infinite Loop (Terminator)

