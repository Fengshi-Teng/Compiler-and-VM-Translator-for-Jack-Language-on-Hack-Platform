def get_labels(symboltable: dict, assembly_codes: str) -> str:
    '''
    The function maintians a symbol table that contains all the pre-defined
    symbols, user-defined variables and labels. The function takes in an symbol
    and its value, add them into the symboltable.

    Input:
        assembly_codes: string, lines of assembly language
        symboltalbe: a dictionary with symbols as keys and their values.
    Output:
        assembly_codes_no_lable: string, lines of assembly language without
            lables.

    '''
    num_line = 0
    assembly_codes_no_lable = []
    for line in assembly_codes.splitlines():
        if line.startswith("("):
            label = line[1:-1].strip()
            symboltable[label] = num_line
        else:
            assembly_codes_no_lable.append(line)
            num_line += 1
    return "\n".join(assembly_codes_no_lable)


def check_symbol(symbol: str, symboltable: dict) -> str:
    '''
    The function maintians a symbol table that contains all the pre-defined
    symbols, user-defined variables and labels. The function takes in an symbol
    and its value, add them into the symboltable.

    Input:
        assembly_codes: string, lines of assembly language
        symboltalbe: a dictionary with symbols as keys and their values.
    Output:
        assembly_codes_no_lable: string, lines of assembly language without
            lables.

    '''
    if symbol in symboltable:
        return symboltable[symbol]
    else:
        symboltable[symbol] = symboltable["variables_num"]
        symboltable["variables_num"] += 1
        return symboltable[symbol]
