// Computes the modulus operation. Given two values stored in R0 and R1,
// finds the remainder of R0 divided by R1 and stores the results in R2.
// Since no division or shifting, this is mplemented using repeated subtraction.

	@R2
	M=0	// mod = 0
	@R0
	D=M	// D = RAM[0]
	@val
	M=D	// val = RAM[0]
	
(LOOP)
	@val
	D=M	// D = val
	@R1
	D=D-M	// D = val - RAM[1]

	// checks for when R0 <= R1
	@END
	D;JLE	// If (val - RAM[1]) <= 0 goto END

	@R2
	M=D	// Store D into mod
	@val
	M=D	// Store D into val
	
	@R1
	D=M-D	// D = RAM[1] - (val - RAM[1])
	@END
	D;JGT	// If (RAM[1] - (val-RAM[1]) > 0 goto END

	@LOOP
	0;JMP	// Goto LOOP
(END)
	@END
	0;JMP	// Infinite Loop (Terminator)