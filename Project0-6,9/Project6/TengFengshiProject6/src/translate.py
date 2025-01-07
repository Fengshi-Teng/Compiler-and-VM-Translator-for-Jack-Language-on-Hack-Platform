from symbols import check_symbol


def translate(assembly_codes: str, symboltable):
    machine_codes = []
    for line in assembly_codes.splitlines():
        if line.startswith("@"):
            binary_codes = translate_A(line, symboltable)
        else:
            binary_codes = translate_C(line)
        machine_codes.append(binary_codes)
    return '\n'.join(machine_codes)


def translate_A(line: str, symboltable: dict) -> str:
    '''
    The function takes in an A-instruction and translates it into binary codes.

    Input: single line string starting with"@"
    Output: single line string, binary codes
    '''
    if line[1:].isdigit():
        num = int(line[1:])
    else:
        num = check_symbol(line[1:], symboltable)
    return format(num, "016b")


def translate_C(line: str) -> str:
    '''
    The function takes in a C-instruction and translates it into binary codes.

    Input: single line string not starting with"@"
    Output: single line string, binary codes
    '''
    destcode = ""
    jumpcode = ""
    remain = line
    if ";" in remain:
        jumpcode = line.split(";")[1]
        remain = line.split(";")[0]
    if "=" in remain:
        destcode = remain.split("=")[0]
        remain = remain.split("=")[1]
    compcode = remain
    return ('111' + translate_comp(compcode) +
            translate_dest(destcode) + translate_jump(jumpcode))


def translate_comp(code: str) -> str:
    '''
    The function takes in a comp code of assembly language and translate it
    into machine code.

    Input: string, computational code of assembly language
    Output: string, 7-bit binary machine code
    '''
    comp_dict = {
        "0": "0101010",
        "1": "0111111",
        "-1": "0111010",
        "D": "0001100",
        "A": "0110000",
        "!D": "0001101",
        "!A": "0110001",
        "-D": "0001111",
        "-A": "0110011",
        "D+1": "0011111",
        "A+1": "0110111",
        "D-1": "0001110",
        "A-1": "0110010",
        "D+A": "0000010",
        "A+D": "0000010",
        "D-A": "0010011",
        "A-D": "0000111",
        "D&A": "0000000",
        "A&D": "0000000",
        "D|A": "0010101",
        "M": "1110000",
        "!M": "1110001",
        "-M": "1110011",
        "M+1": "1110111",
        "M-1": "1110010",
        "D+M": "1000010",
        "M+D": "1000010",
        "D-M": "1010011",
        "M-D": "1000111",
        "D&M": "1000000",
        "M&D": "1000000",
        "D|M": "1010101",
        "M|D": "1010101",
    }
    return comp_dict[code]


def translate_dest(code: str) -> str:
    '''
    The function takes in a dest code of assembly language and translate it
    into machine code.

    Input: string, destination code of assembly language
    Output: string, 3-bit binary machine code
    '''
    dest_dict = {
        "": "000",
        "M": "001",
        "D": "010",
        "MD": "011",
        "A": "100",
        "AM": "101",
        "AD": "110",
        "AMD": "111"
    }
    return dest_dict[code]


def translate_jump(code: str) -> str:
    '''
    The function takes in a jump code of assembly language and translate it
    into machine code.

    Input: string, jump code of assembly language
    Output: string, 3-bit binary machine code
    '''
    jump_dict = {
        "": "000",
        "JGT": "001",
        "JEQ": "010",
        "JGE": "011",
        "JLT": "100",
        "JNE": "101",
        "JLE": "110",
        "JMP": "111"
    }
    return jump_dict[code]
