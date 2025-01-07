|||| PROJECT8 VMTranslator Part2 (VM2)
|||| Fengshi Teng
|||| Nov10, 2024

README

This program is written in Python 3 on MacOS.
This program is a Virtual Machine (VM) translator designed to convert VM
language into Hack Assembly language for execution on the Hack computer. 
The input is a `.vm` file, and the output is a `.asm` file, which contains
translated Hack Assembly code.
The program automatically removes comments and blank lines, performs
modifications on the VM code, and translates it into Hack Assembly language.
For detailed usage and functionality, refer to this document and the associated
code comments.

## How to Run the Program
* How to Run the Program:
If you have Python3:
    Step 1: Decompress the provided .zip file.
    Step 2: Navigate to the directory where the decompressed files are located:
                ______________________________________________
                | bash |
                cd path/to/TengFengshiProject8
                ——————————————————————————————————————————————

    Step 3: Use python and try following command on MacOS, Windows, Linux, as
	    long as you installed python. Use python3 if you encounter a
	    “command not found” error. 
                ______________________________________________
                | bash |
                python src/VM2.py path/to/directory
                ——————————————————————————————————————————————

    Once the program runs successfully, you will see this message:
                ______________________________________________
                | bash |
                Output written to [directory].asm successfully!
                ——————————————————————————————————————————————
    You'll get a new file 'directory_name.asm' in the input directory.

**PLEASE INPUT A DIRECTORY CONTAINING YOUR `.vm` FILE(s), EVEN IF ONLY ONE
FILE NEEDS TO BE TRANSLATED!**  

* Features:
1. **Automatic Comment Removal**:
    - Removes both inline comments (//) and block comments in VM code.
    - Ignores blank lines and trims leading whitespace for cleaner code.

2. **VM to Assembly Translation**:
    - Translates VM commands into Hack Assembly instructions, following the
    Hack machine architecture.
    - Handles arithmetic, logical, and memory access commands, including
    'static' segment handling with unique file-based naming.

* Workflow:
1. **Modification**:
    - Removes blank lines and comments from the VM code.
    - Provides cleaner VM code for translation.
2. **Translation**:
    - Translates modified VM code into Hack Assembly code, using helper
    functions in the 'translation' module.

* Input:
    - A directory containing at least one '.vm' file.

* Output:
    - A '.asm' file with Hack Assembly code translated from the input VM
    commands.
