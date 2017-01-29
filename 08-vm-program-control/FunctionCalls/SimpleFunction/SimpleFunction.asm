(SIMPLEFUNCTION.TEST)
    @2
    D=A
    @R13
    M=D
(SIMPLEFUNCTION.TEST_LCL_START)
    @R13
    MD=M-1
    @SIMPLEFUNCTION.TEST_LCL_END
    D;JLT
    @SP
    M=M+1
    A=M-1
    M=0
    @SIMPLEFUNCTION.TEST_LCL_START
    0;JMP
(SIMPLEFUNCTION.TEST_LCL_END)
// push local 0
    @0
    D=A
    @LCL
    A=M+D
    D=M
    @SP
    M=M+1
    A=M-1
    M=D

// push local 1
    @1
    D=A
    @LCL
    A=M+D
    D=M
    @SP
    M=M+1
    A=M-1
    M=D

// add
    @SP
    AM=M-1
    D=M
    @SP
    AM=M-1
    A=M
    D=A+D
    @SP
    M=M+1
    A=M-1
    M=D

// not
    @SP
    A=M-1
    M=!M

// push argument 0
    @0
    D=A
    @ARG
    A=M+D
    D=M
    @SP
    M=M+1
    A=M-1
    M=D

// add
    @SP
    AM=M-1
    D=M
    @SP
    AM=M-1
    A=M
    D=A+D
    @SP
    M=M+1
    A=M-1
    M=D

// push argument 1
    @1
    D=A
    @ARG
    A=M+D
    D=M
    @SP
    M=M+1
    A=M-1
    M=D

// sub
    @SP
    AM=M-1
    D=M
    @SP
    AM=M-1
    A=M
    D=A-D
    @SP
    M=M+1
    A=M-1
    M=D

    @5
    D=A
    @LCL
    A=M-D
    D=M
    @R14
    M=D
    @SP
    AM=M-1
    D=M
    @ARG
    A=M
    M=D
    @ARG
    D=M+1
    @SP
    M=D
    @LCL
    D=M
    @R13
    M=D
    @R13
    AM=M-1
    D=M
    @THAT
    M=D
    @R13
    AM=M-1
    D=M
    @THIS
    M=D
    @R13
    AM=M-1
    D=M
    @ARG
    M=D
    @R13
    AM=M-1
    D=M
    @LCL
    M=D
    @R14
    A=M
    0;JMP
// Infinite Loop (Terminator)
(END)
    @END
    0;JMP
