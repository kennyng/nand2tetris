// Initialize SP
    @256
    D=A
    @SP
    M=D
    @RET_SYS.INIT_1
    D=A
    @SP
    M=M+1
    A=M-1
    M=D
    @LCL
    D=M
    @SP
    M=M+1
    A=M-1
    M=D
    @ARG
    D=M
    @SP
    M=M+1
    A=M-1
    M=D
    @THIS
    D=M
    @SP
    M=M+1
    A=M-1
    M=D
    @THAT
    D=M
    @SP
    M=M+1
    A=M-1
    M=D
    @0
    D=A
    @5
    D=A+D
    @SP
    D=M-D
    @ARG
    M=D
    @SP
    D=M
    @LCL
    M=D
    @SYS.INIT
    0;JMP
(RET_SYS.INIT_1)
(CLASS1.SET)
    @0
    D=A
    @R13
    M=D
(CLASS1.SET_LCL_START)
    @R13
    MD=M-1
    @CLASS1.SET_LCL_END
    D;JLT
    @SP
    M=M+1
    A=M-1
    M=0
    @CLASS1.SET_LCL_START
    0;JMP
(CLASS1.SET_LCL_END)
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

// pop static 0
    @SP
    AM=M-1
    D=M
    @Class1.0
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

// pop static 1
    @SP
    AM=M-1
    D=M
    @Class1.1
    M=D

// push constant 0
    @0
    D=A
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
(CLASS1.GET)
    @0
    D=A
    @R13
    M=D
(CLASS1.GET_LCL_START)
    @R13
    MD=M-1
    @CLASS1.GET_LCL_END
    D;JLT
    @SP
    M=M+1
    A=M-1
    M=0
    @CLASS1.GET_LCL_START
    0;JMP
(CLASS1.GET_LCL_END)
// push static 0
    @Class1.0
    D=M
    @SP
    M=M+1
    A=M-1
    M=D

// push static 1
    @Class1.1
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
(CLASS2.SET)
    @0
    D=A
    @R13
    M=D
(CLASS2.SET_LCL_START)
    @R13
    MD=M-1
    @CLASS2.SET_LCL_END
    D;JLT
    @SP
    M=M+1
    A=M-1
    M=0
    @CLASS2.SET_LCL_START
    0;JMP
(CLASS2.SET_LCL_END)
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

// pop static 0
    @SP
    AM=M-1
    D=M
    @Class2.0
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

// pop static 1
    @SP
    AM=M-1
    D=M
    @Class2.1
    M=D

// push constant 0
    @0
    D=A
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
(CLASS2.GET)
    @0
    D=A
    @R13
    M=D
(CLASS2.GET_LCL_START)
    @R13
    MD=M-1
    @CLASS2.GET_LCL_END
    D;JLT
    @SP
    M=M+1
    A=M-1
    M=0
    @CLASS2.GET_LCL_START
    0;JMP
(CLASS2.GET_LCL_END)
// push static 0
    @Class2.0
    D=M
    @SP
    M=M+1
    A=M-1
    M=D

// push static 1
    @Class2.1
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
(SYS.INIT)
    @0
    D=A
    @R13
    M=D
(SYS.INIT_LCL_START)
    @R13
    MD=M-1
    @SYS.INIT_LCL_END
    D;JLT
    @SP
    M=M+1
    A=M-1
    M=0
    @SYS.INIT_LCL_START
    0;JMP
(SYS.INIT_LCL_END)
// push constant 6
    @6
    D=A
    @SP
    M=M+1
    A=M-1
    M=D

// push constant 8
    @8
    D=A
    @SP
    M=M+1
    A=M-1
    M=D

    @RET_CLASS1.SET_2
    D=A
    @SP
    M=M+1
    A=M-1
    M=D
    @LCL
    D=M
    @SP
    M=M+1
    A=M-1
    M=D
    @ARG
    D=M
    @SP
    M=M+1
    A=M-1
    M=D
    @THIS
    D=M
    @SP
    M=M+1
    A=M-1
    M=D
    @THAT
    D=M
    @SP
    M=M+1
    A=M-1
    M=D
    @2
    D=A
    @5
    D=A+D
    @SP
    D=M-D
    @ARG
    M=D
    @SP
    D=M
    @LCL
    M=D
    @CLASS1.SET
    0;JMP
(RET_CLASS1.SET_2)
// pop temp 0
    @0
    D=A
    @R5
    D=A+D
    @R13
    M=D
    @SP
    AM=M-1
    D=M
    @R13
    A=M
    M=D

// push constant 23
    @23
    D=A
    @SP
    M=M+1
    A=M-1
    M=D

// push constant 15
    @15
    D=A
    @SP
    M=M+1
    A=M-1
    M=D

    @RET_CLASS2.SET_3
    D=A
    @SP
    M=M+1
    A=M-1
    M=D
    @LCL
    D=M
    @SP
    M=M+1
    A=M-1
    M=D
    @ARG
    D=M
    @SP
    M=M+1
    A=M-1
    M=D
    @THIS
    D=M
    @SP
    M=M+1
    A=M-1
    M=D
    @THAT
    D=M
    @SP
    M=M+1
    A=M-1
    M=D
    @2
    D=A
    @5
    D=A+D
    @SP
    D=M-D
    @ARG
    M=D
    @SP
    D=M
    @LCL
    M=D
    @CLASS2.SET
    0;JMP
(RET_CLASS2.SET_3)
// pop temp 0
    @0
    D=A
    @R5
    D=A+D
    @R13
    M=D
    @SP
    AM=M-1
    D=M
    @R13
    A=M
    M=D

    @RET_CLASS1.GET_4
    D=A
    @SP
    M=M+1
    A=M-1
    M=D
    @LCL
    D=M
    @SP
    M=M+1
    A=M-1
    M=D
    @ARG
    D=M
    @SP
    M=M+1
    A=M-1
    M=D
    @THIS
    D=M
    @SP
    M=M+1
    A=M-1
    M=D
    @THAT
    D=M
    @SP
    M=M+1
    A=M-1
    M=D
    @0
    D=A
    @5
    D=A+D
    @SP
    D=M-D
    @ARG
    M=D
    @SP
    D=M
    @LCL
    M=D
    @CLASS1.GET
    0;JMP
(RET_CLASS1.GET_4)
    @RET_CLASS2.GET_5
    D=A
    @SP
    M=M+1
    A=M-1
    M=D
    @LCL
    D=M
    @SP
    M=M+1
    A=M-1
    M=D
    @ARG
    D=M
    @SP
    M=M+1
    A=M-1
    M=D
    @THIS
    D=M
    @SP
    M=M+1
    A=M-1
    M=D
    @THAT
    D=M
    @SP
    M=M+1
    A=M-1
    M=D
    @0
    D=A
    @5
    D=A+D
    @SP
    D=M-D
    @ARG
    M=D
    @SP
    D=M
    @LCL
    M=D
    @CLASS2.GET
    0;JMP
(RET_CLASS2.GET_5)
(SYS.INIT$WHILE)
    @SYS.INIT$WHILE
    0;JMP
     
// Infinite Loop (Terminator)
(END)
    @END
    0;JMP
