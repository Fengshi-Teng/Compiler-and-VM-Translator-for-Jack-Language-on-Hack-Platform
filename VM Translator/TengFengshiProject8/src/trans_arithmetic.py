'''
This module translates arithmetic and logical VM commands into Hack Assembly
Language for the Hack machine architecture. It includes functions to handle
various VM commands such as 'add', 'sub', 'and', 'or', 'not', 'neg', and
comparison operations ('lt', 'gt', 'eq'). Each function takes a VM command
and returns the corresponding Hack assembly code as a multi-line string.
'''


dict_operation = {
        "add": "D+M",
        "sub": "M-D",
        "and": "D&M",
        "or": "D|M",
        "not": "!M",
        "neg": "-M",
        "gt": "JGT",
        "lt": "JLT",
        "eq": "JEQ"
    }
jump_time = 0


def trans_arith(command: list[str]) -> str:
    '''
    This function translates one line of arithmetic command in VM script into
    Hack Assembly Language.

    Input:
        command - string, arithmetic operation.
    Output:
        asembly_codes - multiple lines of string.
    '''
    if command in ("not", "neg"):
        return one_arg(command)
    if command in ("add", "sub", "and", "or"):
        return two_arg(command)
    if command in ("gt", "lt", "eq"):
        global jump_time
        jump_time += 1
        return compare(command, jump_time)
    return ""


def one_arg(command):
    '''
    This function translates one line of arithmetic command with one argument
    into Hack Assembly Language.

    Input:
        command - string, arithmetic operation 'not', 'neg'.
    Output:
        asembly_codes - multiple lines of string.
    '''
    return "@SP\nA=M-1\nM=" + dict_operation[command] + '\n'


def two_arg(command):
    '''
    This function translates one line of arithmetic command with two arguments
    into Hack Assembly Language.

    Input:
        command - string, arithmetic operation 'add', 'sub', 'and', 'or'.
    Output:
        asembly_codes - multiple lines of string.
    '''
    return "@SP\nAM=M-1\nD=M\nA=A-1\n" + "M=" + dict_operation[command] + '\n'


def compare(command, jump_time):
    '''
    This function translates one line of comparison command into Hack Assembly
    Language.

    Input:
        command - string, arithmetic operation 'lt', 'gt', 'eq'.
        JUMP_time - int, denote different jump labels.
    Output:
        asembly_codes - multiple lines of string.
    '''
    return "@SP\nAM=M-1\nD=M\nA=A-1\nD=M-D\nM=-1\n@CONTINUE" + \
        str(jump_time) + "\nD;" + dict_operation[command] + \
        "\n@SP\nA=M-1\nM=0\n(CONTINUE" + str(jump_time) + ")\n"
