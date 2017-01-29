// push constant 111
    @111
    D=A
    @SP
    M=M+1
    A=M-1
    M=D

// push constant 333
    @333
    D=A
    @SP
    M=M+1
    A=M-1
    M=D

// push constant 888
    @888
    D=A
    @SP
    M=M+1
    A=M-1
    M=D

// pop static 8
    @SP
    AM=M-1
    D=M
    @StaticTest.8
    M=D

// pop static 3
    @SP
    AM=M-1
    D=M
    @StaticTest.3
    M=D

// pop static 1
    @SP
    AM=M-1
    D=M
    @StaticTest.1
    M=D

// push static 3
    @StaticTest.3
    D=M
    @SP
    M=M+1
    A=M-1
    M=D

// push static 1
    @StaticTest.1
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

// push static 8
    @StaticTest.8
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

// Infinite Loop (Terminator)
(END)
    @END
    0;JMP
