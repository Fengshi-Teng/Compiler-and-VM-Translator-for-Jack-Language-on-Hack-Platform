''' Project10-1 Jack Compiler - Tokenizer
    Version 1.0
    Fengshi Teng, NOV28 2024

    This module implements a tokenizer for the Jack programming language. It
    converts Jack source code into a stream of tokens encapsulated in XML tags.
    For more information, please refer to README.
'''

import os
import sys
import glob
from modify import remove_comments1
from modify import remove_comments2


keywords = ('class', 'constructor', 'function', 'method', 'field', 'true',
            'static', 'var', 'int', 'char', 'boolean', 'void', 'return',
            'false', 'null', 'this', 'let', 'do', 'if', 'else', 'while')


def main():
    '''
    Main entry point for the tokenizer.

    This function processes all `.jack` files in the specified directory,
    tokenizes them, and outputs the results as XML files.
    '''
    # get file name and create new file name
    if len(sys.argv) != 2:
        print("Usage: python3 tokenizer.py <directory_input_jack_files>!")
        return
    else:
        input_directory = sys.argv[1]
        input_files = glob.glob(os.path.join(input_directory, "*.jack"))

    print(input_files)
    # tokenize files
    for file in input_files:
        tokenize_files(file)

    return


def tokenize_files(input_file: str):
    '''
    Tokenizes a single `.jack` file and writes the tokenized output to an XML
    file. The output XML file will have the same name as the input file with
    "T.xml" appended.
    '''
    # new file name
    output_file = input_file.rstrip('.jack')+"T.xml"

    # Step1: remove comments and blank spaces
    jack_code = fetch_code(input_file)

    # Step2: tokenizer
    tokenized = tokenize(jack_code)

    # output
    with open(output_file, 'w', encoding="UTF-8") as output:
        for line in tokenized:
            output.write(line)

    # give a feedback
    print(f"Output written to {output_file} successfully!")
    return


def fetch_code(file_name: str) -> str:
    '''
    Fetches and preprocesses the Jack code from the given file.
    This function removes blank lines, leading whitespace, and comments (both
    single-line and multi-line).
    '''
    jack_code = ""
    with open(file_name, 'r', encoding="UTF-8") as file:
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
            jack_code += line
    jack_code = remove_comments2(jack_code)  # Modify4: remove comments type 2
    return jack_code


def tokenize(code: str) -> str:
    '''
    Tokenizes the Jack code into XML tokens.

    The tokenizer recognizes keywords, symbols, identifiers, integer constants,
    and string constants. It outputs the tokens encapsulated in XML tags.

    '''
    # lexical elements
    symbols = ('{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', '*', '/',
               '&', '|', '<', '>', '=', '~')

    # token classify
    pointer = 0
    current_word = ""
    tokenized = "<tokens>\n"
    while pointer < len(code):
        # skip EOLs or blank spaces:
        if code[pointer] == ' ' or code[pointer] == '\n':
            if current_word:
                tokenized += deal_with_word(current_word)
            current_word = ""
        # deal with string constant
        elif code[pointer] == '"':
            current_word += '"'
            pointer += 1
            while code[pointer] != '"':
                current_word += code[pointer]
                pointer += 1
            current_word += '"'
        # deal with symbols
        elif code[pointer] in symbols:
            if current_word:
                tokenized += deal_with_word(current_word)
            current_word = ""
            # deal with "< & >" specially
            if code[pointer] == "<":
                tokenized += '<symbol> &lt; </symbol>\n'
            elif code[pointer] == ">":
                tokenized += '<symbol> &gt; </symbol>\n'
            elif code[pointer] == "&":
                tokenized += '<symbol> &amp; </symbol>\n'
            else:
                tokenized += '<symbol> ' + code[pointer] + ' </symbol>\n'
        # deal with the others
        else:
            current_word += code[pointer]
        pointer += 1
    tokenized += '</tokens>\n'
    return tokenized


def deal_with_word(current_word: str) -> str:
    '''
    Classifies and wraps a word into the appropriate XML token.
    '''
    if current_word.startswith('"'):
        return ('<stringConstant> ' + current_word.strip('"')
                + ' </stringConstant>\n')
    elif current_word.isdigit():
        return '<integerConstant> ' + current_word + ' </integerConstant>\n'
    elif current_word in keywords:
        return '<keyword> ' + current_word + ' </keyword>\n'
    else:
        return '<identifier> ' + current_word + ' </identifier>\n'


if __name__ == "__main__":
    main()
