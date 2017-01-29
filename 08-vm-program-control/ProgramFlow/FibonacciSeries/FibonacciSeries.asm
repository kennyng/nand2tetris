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

// pop pointer 1
    @1
    D=A
    @THIS
    D=A+D
    @R13
    M=D
    @SP
    AM=M-1
    D=M
    @R13
    A=M
    M=D

// push constant 0
    @0
    D=A
    @SP
    M=M+1
    A=M-1
    M=D

// pop that 0
    @0
    D=A
    @THAT
    D=M+D
    @R13
    M=D
    @SP
    AM=M-1
    D=M
    @R13
    A=M
    M=D

// push constant 1
    @1
    D=A
    @SP
    M=M+1
    A=M-1
    M=D

// pop that 1
    @1
    D=A
    @THAT
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

// push constant 2
    @2
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

(FUNCTION_NAME$MAIN_LOOP_START)
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
    @FUNCTION_NAME$COMPUTE_ELEMENT
    D;JNE
     
    @FUNCTION_NAME$END_PROGRAM
    0;JMP
     
(FUNCTION_NAME$COMPUTE_ELEMENT)
// push that 0
    @0
    D=A
    @THAT
    A=M+D
    D=M
    @SP
    M=M+1
    A=M-1
    M=D

// push that 1
    @1
    D=A
    @THAT
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

// pop that 2
    @2
    D=A
    @THAT
    D=M+D
    @R13
    M=D
    @SP
    AM=M-1
    D=M
    @R13
    A=M
    M=D

// push pointer 1
    @1
    D=A
    @THIS
    A=A+D
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

// pop pointer 1
    @1
    D=A
    @THIS
    D=A+D
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

    @FUNCTION_NAME$MAIN_LOOP_START
    0;JMP
     
(FUNCTION_NAME$END_PROGRAM)
// Infinite Loop (Terminator)
(END)
    @END
    0;JMP
