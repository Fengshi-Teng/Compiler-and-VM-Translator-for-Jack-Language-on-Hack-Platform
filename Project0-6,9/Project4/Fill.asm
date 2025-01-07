// Runs an infinite loop that listens to the keyboard input. 
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel. When no key is pressed, 
// the screen should be cleared.


/////// initialization
        @16384
        D=A         // D = 16384
        @i
        M=D         // i = 16384, first pixel of screen

/////// main loop
(WAIT)
        @24576
        D=M         // D = keyborad input
        @WAIT
        D;JEQ       // wait if no input from keyboard

/////// blacken loop
(BLACKEN)
        @i
        A=M         // A = i
        M=-1        // blackens one address
        @i
        MD=M+1      // D,i = i + 1, prepare for next loop

        @24576
        D=D-A       // D = i - 24576
        @KEEP
        D;JEQ       // goto KEEP if (i - 24576) = 0, which means full screen blackened

        @24576
        D=M         // D = keyborad input
        @WHITEN
        D;JEQ       // goto WHITEN loop if no input from keyboard

        @BLACKEN
        0;JMP       // continue BLACKEN loop

/////// whiten loop
(WHITEN)
        @i
        AMD=M-1     // A, D, i= i-1
        M=0         // whiten one address

        @16384
        D=D-A       // D = i - 16384
        @WAIT
        D;JEQ       // goto WAIT if (i - 16384) = 0, which means full screen whitened

        @24576
        D=M         // D = keyborad input
        @BLACKEN
        D;JNE       // goto BLACKEN loop if getting input from keyboard

        @WHITEN
        0;JMP

/////// keep full blakend screen
(KEEP)
        @24576
        D=M         // D = keyborad input
        @WHITEN
        D;JEQ       // goto WHITEN loop if no input from keyboard
        @KEEP
        0;JMP       // goto KEEP loop if input got





