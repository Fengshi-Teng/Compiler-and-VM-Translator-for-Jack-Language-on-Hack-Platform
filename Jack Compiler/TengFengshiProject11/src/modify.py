''' Project0
    Version 1.0
    Fengshi Teng, Oct9 2024

    This program removes comments and white spaces from a text file.
    For detailed usage instructions and additional information, please
    refer to the README.txt file.
'''

import sys


def main():
    '''
    Main function
    '''
    # get file name and create new file name
    if len(sys.argv) != 2:
        print("Usage: python3 program.py <input_string>!")
    else:
        input_file = sys.argv[1]
        output_file = input_file.rstrip('.in')+".out"

    # get content and modify at the same time
    content = ""
    with open(input_file, 'r', encoding="UTF-8") as file:
        for line in file:
            if line.strip() == "":       # Modify1: skip blank lines
                continue
            line = line.lstrip()         # Modify2: remove leading white space
            if '//' in line:             # Modify3: remove comments of type 1
                if line[:2] == "//":
                    continue
                line = remove_comments1(line)
            content += line
    content = remove_comments2(content)  # Modify4: remove comments of type 2

    # output
    with open(output_file, 'w', encoding="UTF-8") as output:
        for line in content:
            output.write(line)

    # give a feedback
    print(f"Output written to {output_file} successfully!")
    return


def remove_comments1(line: str) -> str:
    '''
    The function is used to delete the comment starting with "//"

    Input: single line string with comment starting with "//" not at beginning
    Output: single line string containing the content before the "//"
    '''

    content = line.split("//")
    return content[0].rstrip()+'\n'


def remove_comments2(content: str) -> str:
    '''
    The function is used to delete the multiple line comments

    Input: mutiple line string with comments in "/*...*/"
    Output: mutiple line string with comments stripped
    '''
    reserved_lines = []
    need_deletion = False
    for line in content.splitlines():
        if "/*" in line and "*/" in line:
            reserved_part = ''       # get the outside string
            if line[:2] != "/*":
                reserved_part += line.split("/*")[0]
            if line[-2:] != "*/":
                reserved_part += line.split("*/")[-1]
            if reserved_part:
                reserved_lines.append(reserved_part)
        elif "/*" in line:
            if line[:2] != "/*":    # reserve the part before comment
                reserved_lines.append(line.split("/*")[0])
            need_deletion = True    # set deletion notation
        elif "*/" in line:
            if line[-2:] != "*/":   # reserve the part after comment
                reserved_lines.append(line.split("*/")[-1])
            need_deletion = False   # release deletion notation
        else:
            if not need_deletion:
                reserved_lines.append(line)
    return '\n'.join(reserved_lines)


if __name__ == "__main__":
    main()
