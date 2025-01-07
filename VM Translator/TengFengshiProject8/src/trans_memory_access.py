'''
This module provides functions to translate VM memory access commands into Hack
Assembly Language. It supports 'push' and 'pop' operations for various segments
including 'constant', 'local', 'argument', 'this', 'that', 'pointer', and
'temp'. Special handling is provided for the `static` segment to ensure
unique naming across different files.
'''


dict_segement = {
    "this": "THIS",
    "that": "THAT",
    "argument": "ARG",
    "local": "LCL"
}


def trans_mem(mem_command: list[str]) -> str:
    '''
    This function translates one line of memory access command in VM script
    into Hack Assembly Language. (except for commands with segemt 'static')

    Input:
        mem_command - list of string, memory access operations.
    Output:
        asembly_codes - multiple lines of string.
    '''
    # split the VM code
    command, segment, value = mem_command
    if command == "push":
        return push(segment, value)
    else:
        return pop(segment, value)


def trans_static(mem_command: list[str], file_name: str) -> str:
    '''
    This function translates one line of memory access command  with segemt
    'static' in VM script into Hack Assembly Language.

    Input:
        mem_command - list of string, memory access operations.
    Output:
        asembly_codes - multiple lines of string.
    '''
    command = mem_command[0]
    value = mem_command[2]
    if command == "push":
        return "@" + file_name + "." + value +\
            "\nD=M\n@SP\nAM=M+1\nA=A-1\nM=D\n"
    else:
        return "@SP\nAM=M-1\nD=M\n@" + file_name + "." + value + "\nM=D\n"


def push(segment, value) -> str:
    '''
    Generates Hack assembly code for a 'push' operation for segments other than
    'static'.

    Inputs:
        segment (str): The memory segment to access. Options are 'constant',
                        'local', 'argument', 'this', 'that', 'temp'.
        value (str): The index or value to push onto the stack.

    Output:
        str: Hack assembly code to perform the 'push; operation for the
        specified segment.
    '''
    PUSH = "@SP\nAM=M+1\nA=A-1\nM=D\n"
    if segment == "constant":
        return "@" + value + "\nD=A\n" + PUSH
    if segment == "pointer":
        pointer = "THIS" if value == "0" else "THAT"
        return "@" + pointer + "\nD=M\n" + PUSH
    if segment in ("this", "that", "argument", "local"):
        return "@" + dict_segement[segment] + "\nD=M\n@" + value +\
            "\nA=D+A\nD=M\n" + PUSH
    if segment == "temp":
        return "@" + str(int(value)+5) + "\nD=M\n" + PUSH


def pop(segment, value) -> str:
    '''
    Generates Hack assembly code for a 'pop' operation for segments other than
    'static'.

    Inputs:
        segment (str): The memory segment to access. Options are 'pointer',
                        'local', 'argument', 'this', 'that', 'temp'.
        value (str): The index to pop from the stack.

    Output:
        str: Hack assembly code to perform the 'pop' operation for the
        specified segment.
    '''
    POP = "@SP\nAM=M-1\nD=M\n"
    if segment == "pointer":
        pointer = "THIS" if value == "0" else "THAT"
        return POP + "@" + pointer + "\nM=D\n"
    if segment in ("this", "that", "argument", "local"):
        return "@" + dict_segement[segment] + "\nD=M\n@" + value +\
            "\nD=D+A\n@R13\nM=D\n" + POP + "@R13\nA=M\nM=D\n"
    if segment == "temp":
        return POP + "@" + str(int(value)+5) + "\nM=D\n"
