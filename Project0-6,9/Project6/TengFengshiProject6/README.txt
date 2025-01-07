|||| PROJECT6 ASSEMBLER
|||| Fengshi Teng
|||| Oct16, 2024

README

This program is written in Python 3 on MacOS.

* How to Run the Program:
If you have Python3:
    Step 1: Decompress the provided .zip file.
    Step 2: Navigate to the directory where the decompressed files are located:
                ______________________________________________
                | bash |
                cd path/to/TengFengshiProject6
                ——————————————————————————————————————————————

    Step 3: On MacOS, run the program using the following command, ensuring that 
            the input file ends with .asm. Replace filename with yours:
                ______________________________________________
                | bash |
                assembler path/to/filename.asm
                ——————————————————————————————————————————————
            On Windows, please run:
                ______________________________________________
                | bash |
                .\assembler_win.exe path\to\filename.asm
                ——————————————————————————————————————————————
            You can also use python and try following command on MacOS, 
            Windows, Linux, as long as you installed python. Use python3 if you 
            encounter a “command not found” error. 
                ______________________________________________
                | bash |
                python src/assembler.py path/to/filename.asm
                ——————————————————————————————————————————————

    Once the program runs successfully, you will see this message:
                ______________________________________________
                | bash |
                Output written to [filename].hack successfully!
                ——————————————————————————————————————————————
    You'll got a new file 'filename.hack' in the same directory of 'filename.asm'.

* What This Program Does:
    Input:  filename.asm
    Output: filename.hack
    Translate Hack assembly language into machine codes that can be directly
    runs on the hack CUP Emulator.

* Limitations:
    The program only works with files that are correctly written in Hack 
    assembly language. Please ensure that the input file fully complies with 
    the rules and syntax of Hack assembly language.
