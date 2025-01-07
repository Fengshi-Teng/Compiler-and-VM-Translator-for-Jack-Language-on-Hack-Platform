|||| PROJECT11 Compiler
|||| Fengshi Teng
|||| Dec8, 2024

README

## Overview

This project implements a complete Jack Compiler that translates .jack source
code into .vm intermediate code for the Hack platform. The compiler integrates
multiple stages, including tokenization, parsing, and code generation, forming
a critical component in the Jack-to-Hack compilation pipeline.

## How to Run the Programs

    Prerequisites:
        Ensure Python 3.x is installed on your system.

    Step 1: Decompress the provided .zip file.
    Step 2: Navigate to the directory where the decompressed files are located:
                __________________________________________________________
                | bash |
                cd path/to/TengFengshiProject11
                ——————————————————————————————————————————————————————————

    Step 3: Use python and try the following commands on MacOS, Windows, Linux,
            as long as you have Python installed. Use python3 if you encounter
            a “command not found” error.

                __________________________________________________________
                | bash |
                python3 src/compiler.py path/to/directory_with_jack_files
                ——————————————————————————————————————————————————————————

    Once the compiler runs successfully, you will see this message:
                __________________________________________________________
                | bash |
                Output written to [file_name]T.vm successfully!
                ——————————————————————————————————————————————————————————

    Note: Please put the '.jack' into ONE DIRECTORY and call the directory in
    the command line  directly (even if you have only one file)!

## Workflow

	1.	Input:
	•	Source .jack files located in the specified directory.
	2.	Processing:
	•	Tokenization: Strips comments and whitespace, converts the Jack code
        into XML tokens.
	•	Parsing: Transforms tokenized XML into structured representations.
	•	Code Generation: Produces .vm instructions from the parsed
        representations.
	3.	Output:
	•	.vm files containing the Hack virtual machine code.
