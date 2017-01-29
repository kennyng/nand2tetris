// push constant 17
    @17
    D=A
    @SP
    M=M+1
    A=M-1
    M=D

// push constant 17
    @17
    D=A
    @SP
    M=M+1
    A=M-1
    M=D

// eq
    @SP
    AM=M-1
    D=M
    @SP
    AM=M-1
    A=M
    D=A-D
    @LABEL1_TRUE
    D;JEQ
    @SP
    M=M+1
    A=M-1
    M=0
    @LABEL1_FALSE
    0;JMP
(LABEL1_TRUE)
    @SP
    M=M+1
    A=M-1
    M=-1
(LABEL1_FALSE)

// push constant 892
    @892
    D=A
    @SP
    M=M+1
    A=M-1
    M=D

// push constant 891
    @891
    D=A
    @SP
    M=M+1
    A=M-1
    M=D

// lt
    @SP
    AM=M-1
    D=M
    @SP
    AM=M-1
    A=M
    D=A-D
    @LABEL2_TRUE
    D;JLT
    @SP
    M=M+1
    A=M-1
    M=0
    @LABEL2_FALSE
    0;JMP
(LABEL2_TRUE)
    @SP
    M=M+1
    A=M-1
    M=-1
(LABEL2_FALSE)

// push constant 32767
    @32767
    D=A
    @SP
    M=M+1
    A=M-1
    M=D

// push constant 32766
    @32766
    D=A
    @SP
    M=M+1
    A=M-1
    M=D

// gt
    @SP
    AM=M-1
    D=M
    @SP
    AM=M-1
    A=M
    D=A-D
    @LABEL3_TRUE
    D;JGT
    @SP
    M=M+1
    A=M-1
    M=0
    @LABEL3_FALSE
    0;JMP
(LABEL3_TRUE)
    @SP
    M=M+1
    A=M-1
    M=-1
(LABEL3_FALSE)

// push constant 56
    @56
    D=A
    @SP
    M=M+1
    A=M-1
    M=D

// push constant 31
    @31
    D=A
    @SP
    M=M+1
    A=M-1
    M=D

// push constant 53
    @53
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

// push constant 112
    @112
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

// neg
    @SP
    A=M-1
    M=-M

// and
    @SP
    AM=M-1
    D=M
    @SP
    AM=M-1
    A=M
    D=A&D
    @SP
    M=M+1
    A=M-1
    M=D

// push constant 82
    @82
    D=A
    @SP
    M=M+1
    A=M-1
    M=D

// or
    @SP
    AM=M-1
    D=M
    @SP
    AM=M-1
    A=M
    D=A|D
    @SP
    M=M+1
    A=M-1
    M=D

// Infinite Loop (Terminator)
(END)
    @END
    0;JMP
