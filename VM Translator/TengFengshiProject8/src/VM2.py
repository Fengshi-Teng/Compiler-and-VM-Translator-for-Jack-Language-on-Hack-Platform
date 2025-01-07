''' Project8 VM Translator 2
    Version 2.0
    Fengshi Teng, NOV10 2024

    This program is a Virtual Machine (VM) translator designed to convert VM
    language into Hack Assembly language, executable on the Hack computer. The
    input is a `.vm` file, and the output is a `.asm` file. This program
    automatically processes and removes comments and blank lines, performs
    basic modifications on the VM code, and translates it into Hack Assembly
    code. For detailed usage, functionality, and limitations, please refer to
    the README file.
'''

import os
import sys
import glob
from modify import remove_comments1
from modify import remove_comments2
from translation import translate
from trans_control import trans_func


def main():
    # get file name and create new file name
    if len(sys.argv) != 2:
        print("Usage: python3 program.py <input_vm_files> <output_asm_file>!")
        return
    else:
        input_directory = sys.argv[1]
        folder_name = os.path.basename(os.path.normpath(input_directory))
        output_file = os.path.join(input_directory, folder_name + ".asm")
        input_files = glob.glob(os.path.join(input_directory, "*.vm"))

    # translate files:
    assembly_codes = ("@256\nD=A\n@SP\nM=D\n" +
                      trans_func("call Sys.init 0".split()))
    for file in input_files:
        assembly_codes += translate_file(file)

    # output
    with open(output_file, 'w', encoding="UTF-8") as output:
        for line in assembly_codes:
            output.write(line)

    # give a feedback
    print(f"Output written to {output_file} successfully!")
    return


def translate_file(file: str):
    '''
    Perform code modifications and translation.
    '''
    # Step1: modification
    file_name = os.path.basename(file).rstrip(".vm")  # used for static
    vm_codes = ""
    with open(file, 'r', encoding="UTF-8") as file:
        for line in file:
            if line.strip() == "":       # Modify1: skip blank lines
                continue
            line = line.lstrip()         # Modify2: remove leading white space
            if '//' in line:             # Modify3: remove comments of type 1
                if line[:2] == "//":
                    continue
                line = remove_comments1(line)
            else:
                line = line.rstrip() + "\n"
            vm_codes += line
    vm_codes = remove_comments2(vm_codes)  # Modify4: remove comments of type 2
    # Step2: translation
    assembly_codes = translate(vm_codes, file_name)

    return assembly_codes


if __name__ == "__main__":
    main()
