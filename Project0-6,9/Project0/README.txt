|||| PROJECT0 FILE_MODIFIER
|||| Fengshi Teng
|||| October9, 2024

README

This program is written in Python 3 on MacOS.

* How to Run the Program:
If you have Python3:
    Step 1: Decompress the provided .zip file.
    Step 2: Navigate to the directory where the decompressed files are located:
                ______________________________________________
                | bash |
                cd path/to/TengFengshiProject0
                ——————————————————————————————————————————————

    Step 3: On MacOS, run the program using the following command, ensuring that 
            the input file ends with .in. Replace filename with yours:
                ______________________________________________
                | bash |
                ./modify path/to/filename.in
                ——————————————————————————————————————————————
            On Windows, please run:
                ______________________________________________
                | bash |
                .\modify_win.exe path\to\filename.in
                ——————————————————————————————————————————————
            You can alse please use python and try following command on MacOS, 
            Windows, Linux, as long as you installed python. Use python3 if you 
            encounter a “command not found” error. 
                ______________________________________________
                | bash |
                python src/main.py path/to/filename.in
                ——————————————————————————————————————————————

    Once the program runs successfully, you will see this message:
                ______________________________________________
                | bash |
                Output written to [filename].out successfully!
                ——————————————————————————————————————————————
    You'll got a new file 'filename.out' in the same directory of 'filename.in'.

* What This Program Does:
    Input:  filename.in
    Output: filename.out
	1.	Removes blank lines and leading white spaces in the input file.
	2.	Removes single-line comments that begin with // and extend to the end of
        the line:
		    eg. // This comment has no code ahead.
	 	    eg. content // This comment follows some code.
	3.	Removes multi-line comments that begin with /* and end with */, including
        cases that span multiple lines:
	 	    eg. /* This is a single line comment. */
	 	    eg. /* This comment
                    spans multiple lines */
            eg. code /* comment 
                    spans multiple
                    liens */ more code
            eg. This is an /* quite simple */ example.

* Limitations:
    The program cannot remove nested comments (i.e., comments within comments). 
    Please ensure your input file does not contain nested comments.