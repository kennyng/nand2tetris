// push constant 0
    @0
    D=A
    @SP
    M=M+1
    A=M-1
    M=D

// pop local 0
    @0
    D=A
    @LCL
    D=M+D
    @R13
    M=D
    @SP
    AM=M-1
    D=M
    @R13
    A=M
    M=D

(FUNCTION_NAME$LOOP_START)
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

// pop local 0
    @0
    D=A
    @LCL
    D=M+D
    @R13
    M=D
    @SP
    AM=M-1
    D=M
    @R13
    A=M
    M=D

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

// push constant 1
    @1
    D=A
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

// pop argument 0
    @0
    D=A
    @ARG
    D=M+D
    @R13
    M=D
    @SP
    AM=M-1
    D=M
    @R13
    A=M
    M=D

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

    @SP
    AM=M-1
    D=M
    @FUNCTION_NAME$LOOP_START
    D;JNE
     
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

// Infinite Loop (Terminator)
(END)
    @END
    0;JMP
