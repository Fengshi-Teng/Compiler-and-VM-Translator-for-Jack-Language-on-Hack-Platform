'''
This module provides functions for translating Virtual Machine (VM) commands
into Hack Assembly Language. It supports the translation of arithmetic, logical
and memory access commands, converting each line of VM code into its
corresponding Hack assembly instructions.
'''

from trans_arithmetic import trans_arith
from trans_memory_access import trans_mem
from trans_memory_access import trans_static
from trans_control import trans_flow
from trans_control import trans_func


def translate(vm_codes: str, file_name: str):
    '''
    Translates a VM script (multi-line string) into Hack Assembly Language.
    Each line in the VM script is processed to determine if it is an memory
    access, arithmetic, flow controlling or function command. The resulting
    Hack assembly code for each command is concatenated into a single output.

    Inputs:
        vm_codes (str): The entire VM code as a multi-line string, where each
                        line represents a VM command.
        file_name (str): The name of the translated file.

    Output:
        str: A multi-line string containing the Hack assembly code equivalent
             to the input VM commands.
    '''
    assembly_codes = ""
    for line in vm_codes.splitlines():
        code = line.split(" ")
        assembly_codes += '//' + " ".join(code) + "\n"
        # translate arithmetic command
        if len(code) == 1 and code[0] != "return":
            assembly_codes += trans_arith(code[0])
        # translate memory access command
        if code[0] in ['push', 'pop']:
            # deal with command with segment of "static" specially
            if code[1] == "static":
                assembly_codes += trans_static(code, file_name)
                continue
            assembly_codes += trans_mem(code)
        if code[0] in ['label', 'goto', 'if-goto']:
            # translate flow command
            assembly_codes += trans_flow(code)
        if code[0] in ['function', 'call', 'return']:
            # translate function command
            assembly_codes += trans_func(code)
    return assembly_codes
