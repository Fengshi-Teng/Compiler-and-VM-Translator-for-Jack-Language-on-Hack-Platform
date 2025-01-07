// This program multiplies the values found in memory location 0 (R0) and memory location 1 (R1) and stores the result in memory location 2 (R2)
    // initialization
        @i      // i refers to some mem. location; used to record the times of multiplies
        M=1     // i = 1
        @R2     // R2 refers to some mem. location; used to store the result
        M=0     // R2 = 0
(LOOP)
    // loop condition: when i <= R1
        @i
        D=M     // D = i
        @R1
        D=D-M   // i = i-R1
        @END
        D;JGT   // if (i-R1)>0 goto END
    // loop body
        @R0
        D=M     // D = R0
        @R2
        M=M+D   // R2 = R2 + R0
        @i
        M=M+1   // i = i + 1
        @LOOP
        0;JMP   // goto LOOP
(END)
    // ending
        @END
        0;JMP   // infinite loop
