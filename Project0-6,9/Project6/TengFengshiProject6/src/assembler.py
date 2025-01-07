''' Project6 Assembler
    Version 1.0
    Fengshi Teng, Oct26 2024

    This program is a Assembler used to translate Hack Assembly languge to
    Machine language. The input file is a '.asm' file and out put file is a
    '.hack' file. The program automatically removes the commends and get 
    assembly language into binary codes.
'''


import sys
from modify import remove_comments1
from modify import remove_comments2
from symbols import get_labels
from translate import translate


def main():
    # get file name and create new file name
    if len(sys.argv) != 2:
        print("Usage: python3 program.py <input_string>!")
    else:
        input_file = sys.argv[1]
        output_file = input_file.rstrip('.asm')+".hack"

    # Step1: modification
    assembly_codes = ""
    with open(input_file, 'r', encoding="UTF-8") as file:
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
            assembly_codes += line
    assembly_codes = remove_comments2(assembly_codes)  # Modify4: remove comments of type 2

    # Step2: initialize the symbol table
    symboltable = {
        "variables_num": 16,
        "SP": 0,
        "LCL": 1,
        "ARG": 2,
        "THIS": 3,
        "THAT": 4,
        "R0": 0,
        "R1": 1,
        "R2": 2,
        "R3": 3,
        "R4": 4,
        "R5": 5,
        "R6": 6,
        "R7": 7,
        "R8": 8,
        "R9": 9,
        "R10": 10,
        "R11": 11,
        "R12": 12,
        "R13": 13,
        "R14": 14,
        "R15": 15,
        "SCREEN": 16384,
        "KBD": 24576
    }

    # Step3: get all the lables
    assembly_codes = get_labels(symboltable, assembly_codes)

    # Step4: translation
    machine_codes = translate(assembly_codes, symboltable)

    # output
    with open(output_file, 'w', encoding="UTF-8") as output:
        for line in machine_codes:
            output.write(line)

    # give a feedback
    print(f"Output written to {output_file} successfully!")
    return


if __name__ == "__main__":
    main()
