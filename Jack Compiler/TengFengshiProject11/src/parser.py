''' Project10-1 Jack Compiler - Parser
    Version 1.0
    Fengshi Teng, NOV28 2024

    This script implements a parser for the Jack language, converting tokenized
    code into structured XML representations. For more information, please
    refer to README.
'''

import os
import sys
import glob
from tokenizer import fetch_code, tokenize


keywords = ('class', 'constructor', 'function', 'method', 'field', 'true',
            'static', 'var', 'int', 'char', 'boolean', 'void', 'return',
            'false', 'null', 'this', 'let', 'do', 'if', 'else', 'while')


def main():
    # get file name and create new file name
    if len(sys.argv) != 2:
        print("Usage: python3 tokenizer.py <directory_input_jack_files>!")
        return
    else:
        input_directory = sys.argv[1]
        input_files = glob.glob(os.path.join(input_directory, "*.jack"))

    # tokenize files
    for file in input_files:
        parse_files(file)

    return


def parse_files(input_file: str):
    '''
    Tokenizes and parses a single Jack file, writing the parsed XML output.
    '''
    # new file name
    output_file = input_file.rstrip('.jack')+".xml"

    # Step1: remove comments and blank spaces
    jack_code = fetch_code(input_file)

    # Step2: tokenizer
    tokenized = tokenize(jack_code)

    # Step3: parse
    parsed = parse(tokenized)

    # output
    with open(output_file, 'w', encoding="UTF-8") as output:
        for line in parsed:
            output.write(line)

    # give a feedback
    print(f"Output written to {output_file} successfully!")
    return


#  parse #####################################################################
dec = (
    "<keyword> class </keyword>",
    "<keyword> static </keyword>",
    "<keyword> field </keyword>",
    "<keyword> constructor </keyword>",
    "<keyword> function </keyword>",
    "<keyword> method </keyword>",
    "<keyword> var </keyword>"
)


def parse(tokenized: str) -> str:
    '''
    Parses tokenized Jack code into structured XML.
    '''
    tokenized_list = []
    ptr = 0
    parsed = ''
    for line in tokenized.splitlines():
        if line not in ('<tokens>', '</tokens>'):
            tokenized_list.append(line)
    while ptr < len(tokenized_list) and tokenized_list[ptr]:
        if tokenized_list[ptr] in dec:
            parsed_plus, ptr = par_dec("", tokenized_list, ptr)
            parsed += parsed_plus
        else:
            parsed_plus, ptr = par_statements("", tokenized_list, ptr)
            parsed += parsed_plus
    return parsed


#  par dec  ##################################################################

def par_dec(indent: str, code: list, ptr: int):
    '''
    Parses different types of declarations (class, class variable, subroutine).
    '''
    parsed = ''
    if code[ptr] == "<keyword> class </keyword>":
        parsed_plus, ptr = par_class_dec(indent, code, ptr)
    elif code[ptr] in ("<keyword> static </keyword>",
                       "<keyword> field </keyword>"):
        parsed_plus, ptr = par_class_var_dec(indent, code, ptr)
    elif code[ptr] in ("<keyword> constructor </keyword>",
                       "<keyword> function </keyword>",
                       "<keyword> method </keyword>",):
        parsed_plus, ptr = par_subroutine_dec(indent, code, ptr)
    else:
        parsed_plus, ptr = par_var_dec(indent, code, ptr)
    parsed += parsed_plus
    return parsed, ptr


def par_class_dec(indent: str, code: list, ptr: int):
    '''
    Parses a class declaration.
    '''
    parsed = indent + '<class>\n'
    parsed += indent + '  ' + code[ptr] + "\n"  # class
    ptr += 1
    parsed += indent + '  ' + code[ptr] + "\n"  # identifier
    ptr += 1
    parsed += indent + '  ' + code[ptr] + "\n"  # {
    ptr += 1
    while code[ptr] != "<symbol> } </symbol>":
        if code[ptr] in dec:
            parsed_plus, ptr = par_dec(indent + '  ', code, ptr)
            parsed += parsed_plus
        else:
            parsed_plus, ptr = par_statements(indent + '  ', code, ptr)
            parsed += parsed_plus
    parsed += indent + '  ' + code[ptr] + "\n"  # }
    ptr += 1
    parsed += indent + "</class>\n"
    return parsed, ptr


def par_class_var_dec(indent: str, code: list, ptr: int):
    '''
    field/static
    '''
    parsed = indent + '<classVarDec>\n'
    parsed += indent + '  ' + code[ptr] + "\n"  # field/static
    ptr += 1
    parsed += indent + '  ' + code[ptr] + "\n"  # type
    ptr += 1
    while code[ptr] != "<symbol> ; </symbol>":
        parsed += indent + '  ' + code[ptr] + "\n"  # identifier
        ptr += 1
    parsed += indent + '  ' + code[ptr] + "\n"  # ;
    ptr += 1
    parsed += indent + '</classVarDec>\n'
    return parsed, ptr


def par_subroutine_dec(indent: str, code: list, ptr: int):
    '''
    constructor/function/method
    '''
    parsed = indent + '<subroutineDec>\n'
    parsed += indent + '  ' + code[ptr] + "\n"  # constructor/function/method
    ptr += 1
    parsed += indent + '  ' + code[ptr] + "\n"  # void | type
    ptr += 1
    parsed += indent + '  ' + code[ptr] + "\n"  # sobroutineName
    ptr += 1

    parsed += indent + '  ' + code[ptr] + "\n"  # (
    ptr += 1
    parsed += indent + '  <parameterList>\n'
    while code[ptr] != "<symbol> ) </symbol>":   # parameterList
        parsed += indent + '    ' + code[ptr] + "\n"
        ptr += 1
    parsed += indent + '  </parameterList>\n'
    parsed += indent + '  ' + code[ptr] + "\n"  # )
    ptr += 1

    parsed += indent + '  <subroutineBody>\n'
    parsed += indent + '    ' + code[ptr] + "\n"  # {
    ptr += 1
    while code[ptr] != "<symbol> } </symbol>":   # subroutineBody
        if code[ptr] in dec:
            parsed_plus, ptr = par_dec(indent + '    ', code, ptr)
            parsed += parsed_plus
        else:
            parsed_plus, ptr = par_statements(indent + '    ', code, ptr)
            parsed += parsed_plus
    parsed += indent + '    ' + code[ptr] + "\n"  # }
    ptr += 1
    parsed += indent + '  </subroutineBody>\n'

    parsed += indent + '</subroutineDec>\n'
    return parsed, ptr


def par_var_dec(indent: str, code: list, ptr: int):
    '''
    Parses a class variable declaration (static/field).
    '''
    parsed = indent + '<varDec>\n'
    parsed += indent + '  ' + code[ptr] + "\n"  # var
    ptr += 1
    parsed += indent + '  ' + code[ptr] + "\n"  # type
    ptr += 1
    while code[ptr] != "<symbol> ; </symbol>":
        parsed += indent + '  ' + code[ptr] + "\n"  # identifier
        ptr += 1
    parsed += indent + '  ' + code[ptr] + "\n"  # ;
    ptr += 1
    parsed += indent + '</varDec>\n'
    return parsed, ptr


#  par statement #############################################################
statement = (
    "<keyword> let </keyword>",
    "<keyword> if </keyword>",
    "<keyword> while </keyword>",
    "<keyword> do </keyword>",
    "<keyword> return </keyword>"
)


def par_statements(indent: str, code: list, ptr: int):
    '''
    Parses a series of statements and wraps them in a <statements> XML tag.
    '''
    parsed = indent + "<statements>\n"
    while code[ptr] in statement:
        if code[ptr] == "<keyword> let </keyword>":
            parsed_plus, ptr = par_let(indent+'  ', code, ptr)
            parsed += parsed_plus
        elif code[ptr] == "<keyword> if </keyword>":
            parsed_plus, ptr = par_if(indent+'  ', code, ptr)
            parsed += parsed_plus
        elif code[ptr] == "<keyword> while </keyword>":
            parsed_plus, ptr = par_while(indent+'  ', code, ptr)
            parsed += parsed_plus
        elif code[ptr] == "<keyword> do </keyword>":
            parsed_plus, ptr = par_do(indent+'  ', code, ptr)
            parsed += parsed_plus
        else:
            parsed_plus, ptr = par_return(indent+'  ', code, ptr)
            parsed += parsed_plus
    parsed += indent + "</statements>\n"
    return parsed, ptr


def par_let(indent: str, code: list, ptr: int):
    '''
    Parses a let statement and wraps it in a <letStatement> XML tag.
    '''
    parsed = indent + "<letStatement>\n"
    parsed += indent + "  " + code[ptr] + "\n"  # let
    ptr += 1
    parsed += indent + "  " + code[ptr] + "\n"  # identifier
    ptr += 1
    if code[ptr] == "<symbol> [ </symbol>":
        parsed += indent + "  " + code[ptr] + "\n"  # [
        ptr += 1
        parsed_plus, ptr = par_expression(indent + "  ", code, ptr)  # expr
        parsed += parsed_plus
        parsed += indent + "  " + code[ptr] + "\n"  # ]
        ptr += 1
    parsed += indent + "  " + code[ptr] + "\n"  # =
    ptr += 1
    parsed_plus, ptr = par_expression(indent + "  ", code, ptr)  # expr
    parsed += parsed_plus
    parsed += indent + "  " + code[ptr] + "\n"  # ;
    ptr += 1
    parsed += indent + "</letStatement>\n"
    return parsed, ptr


def par_if(indent: str, code: list, ptr: int):
    '''
    Parses an if statement and wraps it in an <ifStatement> XML tag.
    '''
    parsed = indent + "<ifStatement>\n"
    parsed += indent + "  " + code[ptr] + "\n"  # if
    ptr += 1
    parsed += indent + "  " + code[ptr] + "\n"  # (
    ptr += 1
    parsed_plus, ptr = par_expression(indent + "  ", code, ptr)  # expression
    parsed += parsed_plus
    parsed += indent + "  " + code[ptr] + "\n"  # )
    ptr += 1
    parsed += indent + "  " + code[ptr] + "\n"  # {
    ptr += 1
    parsed_plus, ptr = par_statements(indent + "  ", code, ptr)  # statement
    parsed += parsed_plus
    parsed += indent + "  " + code[ptr] + "\n"  # }
    ptr += 1
    if code[ptr] == "<keyword> else </keyword>":
        parsed += indent + "  " + code[ptr] + "\n"  # else
        ptr += 1
        parsed += indent + "  " + code[ptr] + "\n"  # {
        ptr += 1
        parsed_plus, ptr = par_statements(indent + "  ", code, ptr)  # stm
        parsed += parsed_plus
        parsed += indent + "  " + code[ptr] + "\n"  # }
        ptr += 1
    parsed += indent + "</ifStatement>\n"
    return parsed, ptr


def par_while(indent: str, code: list, ptr: int):
    '''
    Parses a while statement and wraps it in a <whileStatement> XML tag.
    '''
    parsed = indent + "<whileStatement>\n"
    parsed += indent + "  " + code[ptr] + "\n"  # while
    ptr += 1
    parsed += indent + "  " + code[ptr] + "\n"  # (
    ptr += 1
    parsed_plus, ptr = par_expression(indent + "  ", code, ptr)  # expression
    parsed += parsed_plus
    parsed += indent + "  " + code[ptr] + "\n"  # )
    ptr += 1
    parsed += indent + "  " + code[ptr] + "\n"  # {
    ptr += 1
    parsed_plus, ptr = par_statements(indent + "  ", code, ptr)  # statements
    parsed += parsed_plus
    parsed += indent + "  " + code[ptr] + "\n"  # }
    ptr += 1
    parsed += indent + "</whileStatement>\n"
    return parsed, ptr


def par_do(indent: str, code: list, ptr: int):
    '''
    Parses a do statement and wraps it in a <doStatement> XML tag.
    '''
    parsed = indent + "<doStatement>\n"
    parsed += indent + "  " + code[ptr] + "\n"  # do
    ptr += 1
    parsed_plus, ptr = par_subroutine_call(indent + "  ", code, ptr)
    parsed += parsed_plus
    parsed += indent + "  " + code[ptr] + "\n"  # ;
    ptr += 1
    parsed += indent + "</doStatement>\n"
    return parsed, ptr


def par_return(indent: str, code: list, ptr: int):
    '''
    Parses a return statement and wraps it in a <returnStatement> XML tag.
    '''
    parsed = indent + "<returnStatement>\n"
    parsed += indent + "  " + code[ptr] + "\n"  # return
    ptr += 1
    if code[ptr] != "<symbol> ; </symbol>":
        parsed_plus, ptr = par_expression(indent + "  ", code, ptr)  # expr
        parsed += parsed_plus
    parsed += indent + "  " + code[ptr] + "\n"  # ,
    ptr += 1
    parsed += indent + "</returnStatement>\n"
    return parsed, ptr


#  par expression  ###########################################################
op = (
    "<symbol> + </symbol>",
    "<symbol> - </symbol>",
    "<symbol> * </symbol>",
    "<symbol> / </symbol>",
    "<symbol> & </symbol>",
    "<symbol> | </symbol>",
    "<symbol> < </symbol>",
    "<symbol> > </symbol>",
    "<symbol> = </symbol>"
)
unaryOp = (
    "<symbol> - </symbol>",
    "<symbol> ~ </symbol>"
)
keyword_constant = (
    "<keyword> true </keyword>",
    "<keyword> false </keyword>",
    "<keyword> null </keyword>",
    "<keyword> this </keyword>"
)
terminate = (
    "<symbol> ) </symbol>",
    "<symbol> ; </symbol>",
    "<symbol> ] </symbol>",
    "<symbol> , </symbol>"
)


def par_expression(indent: str, code: list, ptr: int):
    '''
    Parses an expression and wraps it in an <expression> XML tag.
    An expression consists of terms separated by operators. This function
    processes the terms and operators in sequence and handles nested
    expressions.
    '''
    parsed = indent + "<expression>\n"
    parsed_plus, ptr = par_term(indent+'  ', code, ptr)  # term
    parsed += parsed_plus
    while code[ptr] not in terminate:
        parsed += indent + "  " + code[ptr] + "\n"  # operator
        ptr += 1
        parsed_plus, ptr = par_term(indent + "  ", code, ptr)  # term
        parsed += parsed_plus
    parsed += indent + "</expression>\n"
    return parsed, ptr


def par_term(indent: str, code: list, ptr: int):
    '''
    Parses a term and wraps it in a <term> XML tag.
    '''
    parsed = indent + "<term>\n"
    if code[ptr] == "<symbol> ( </symbol>":  # (expression)
        parsed += indent + "  " + code[ptr] + "\n"  # (
        ptr += 1
        parsed_plus, ptr = par_expression(indent + "  ", code, ptr)  # expr
        parsed += parsed_plus
        parsed += indent + "  " + code[ptr] + "\n"  # )
        ptr += 1
    elif code[ptr] in unaryOp:  # unaryOp + term
        parsed += indent + "  " + code[ptr] + "\n"  # -/~
        ptr += 1
        parsed_plus, ptr = par_term(indent + "  ", code, ptr)  # term
        parsed += parsed_plus
    elif code[ptr].startswith("<identifier>"):  # varName
        if code[ptr+1] in ("<symbol> ( </symbol>", "<symbol> . </symbol>"):
            parsed_plus, ptr = par_subroutine_call(indent + "  ", code, ptr)
            parsed += parsed_plus
        else:
            parsed += indent + "  " + code[ptr] + "\n"  # identifier
            ptr += 1
            if code[ptr] == "<symbol> [ </symbol>":
                parsed += indent + "  " + code[ptr] + "\n"  # [
                ptr += 1
                parsed_plus, ptr = par_expression(indent + "  ", code, ptr)
                parsed += parsed_plus
                parsed += indent + "  " + code[ptr] + "\n"  # ]
                ptr += 1
    else:  # integerConstant/ stringConstant/ keywordConstant
        parsed += indent + "  " + code[ptr] + "\n"
        ptr += 1
    parsed += indent + "</term>\n"
    return parsed, ptr


def par_subroutine_call(indent: str, code: list, ptr: int):
    '''
    Parses a subroutine call and wraps it in the corresponding XML tags.
    '''
    parsed = ""
    parsed += indent + code[ptr] + "\n"  # identifier
    ptr += 1
    if code[ptr] == "<symbol> . </symbol>":
        parsed += indent + code[ptr] + "\n"  # .
        ptr += 1
        parsed += indent + code[ptr] + "\n"  # identifier
        ptr += 1
    parsed += indent + code[ptr] + "\n"  # (
    ptr += 1
    parsed += indent + '<expressionList>\n'
    while True:   # parameterList
        if code[ptr] == "<symbol> ) </symbol>":
            break
        parsed_plus, ptr = par_expression(indent + "  ", code, ptr)  # expr
        parsed += parsed_plus
        if code[ptr] == "<symbol> ) </symbol>":
            break
        parsed += indent + "  " + code[ptr] + "\n"  # ,
        ptr += 1
    parsed += indent + '</expressionList>\n'
    parsed += indent + code[ptr] + "\n"  # )
    ptr += 1
    return parsed, ptr


if __name__ == "__main__":
    main()
