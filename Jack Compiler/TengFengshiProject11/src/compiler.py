''' Project11 Jack Compiler
    Version 1.0
    Fengshi Teng, DEC8 2024

    This script implements a Jack compiler that translates `.jack` source files 
    into `.vm` intermediate code. The compiler processes input Jack files by:
    1. Tokenizing the Jack code.
    2. Parsing the tokens into structured representations.
    3. Generating `.vm` code for the Hack virtual machine.
'''

import os
import sys
import glob
from tokenizer import fetch_code, tokenize
from parser import parse

jumplabel = 0

def main():
    # get file name and create new file name
    if len(sys.argv) != 2:
        print("Usage: python3 tokenizer.py <directory_input_jack_files>!")
        return
    else:
        input_directory = sys.argv[1]
        input_files = glob.glob(os.path.join(input_directory, "*.jack"))

    # compile files
    for file in input_files:
        compile_files(file)

    return


def compile_files(input_file: str):
    '''
    Tokenizes and parses a single Jack file, writing the parsed XML output.
    '''
    # new file name
    output_file = input_file.rstrip('.jack')+".vm"

    # Step1: remove comments and blank spaces
    jack_code = fetch_code(input_file)

    # Step2: tokenizer
    tokenized = tokenize(jack_code)

    # Step3: parse
    parsed = parse(tokenized)

    # Step4: code generation
    VMcode = code_generate(parsed)

    # output
    with open(output_file, 'w', encoding="UTF-8") as output:
        for line in VMcode:
            output.write(line)

    # give a feedback
    print(f"Output written to {output_file} successfully!")
    return



def code_generate(parsed):
    '''
    Generates VM code from parsed Jack code.
    '''
    code_to_compile = Complier(parsed.splitlines())
    code_to_compile.compile_all()
    return code_to_compile.VMcode

###########################################################################
###########################################################################


class Var():
    '''
    Initializes a variable symbol.
    '''
    def __init__(self, name, var_type, kind, index):
        self.name = name
        self.type = var_type
        self.kind = kind
        self.index = index

    def __repr__(self):
        return self.name


class JackClass():
    '''
    A Jack class representation for the Jack compiler.
    '''
    def __init__(self, name):
        self.name = name
        self.vars = {}
        self.static_symbols = 0
        self.field_symbols = 0
        self.subroutines = {}

    def add_field(self, name, var_type):
        '''
        Add a field symbol to the class.
        '''
        self.vars[name] = Var(name, var_type, 'field', self.field_symbols)
        self.field_symbols += 1

    def add_static(self, name, var_type):
        '''
        Add a static symbol to the class.
        '''
        self.vars[name] = Var(name, var_type, 'static',  self.static_symbols)
        self.static_symbols += 1

    def get_symbol(self, name):
        '''
        Get a symbol from the class.
        '''
        return self.vars.get(name)

class JackSubroutine():
    '''
    A Jack subroutine representation for the Jack compiler.
    '''

    def __init__(self, name, subroutine_type, return_type, jack_class):
        self.name = name
        self.jack_class = jack_class
        self.subroutine_type = subroutine_type
        self.return_type = return_type

        self.vars = {}
        self.arg_symbols = 0
        self.var_symbols = 0

        if subroutine_type == 'method':
            self.add_arg('this', self.jack_class.name)

    def add_arg(self, name, var_type):
        '''
        Add an arg symbol to the class.
        '''
        self.vars[name] = Var(name, var_type, 'arg',  self.arg_symbols)
        self.arg_symbols += 1

    def add_var(self, name, var_type):
        '''
        Add a var symbol to the class.
        '''
        self.vars[name] = Var(name, var_type, 'var',  self.var_symbols)
        self.var_symbols += 1

    def get_symbol(self, name):
        '''
        Get a symbol from within the scope of the subroutine.
        '''
        symbol = self.vars.get(name)
        if symbol is not None:
            return symbol
        return self.jack_class.get_symbol(name)


class Complier():
    op_dic = {
        "+": 'add\n',
        "-": 'sub\n',
        "*": 'call Math.multiply 2\n',
        "/": 'call Math.divide 2\n',
        "&amp;": 'and\n',
        "|": 'or\n',
        "&lt;": 'lt\n',
        "&gt;": 'gt\n',
        "=": 'eq\n'
    }
    unaryOp_dic = {
        "-": 'neg\n',
        "~": 'not\n'
    }
    mem_seg = {
        'static': 'static',
        'field': 'this',
        'arg': 'argument',
        'var': 'local'
    }

    def __init__(self, list_code):
        self.content = list_code
        self.VMcode = []
        self.VarTable = []
        # self.structure, self.component = self.create_structure()
        self.structure = self.create_structure(0, len(self.content))

    def compile_all(self):
        '''
        Compiles the entire Jack class into VM code.
        Processes the class structure, variable declarations, subroutines,
        and statements to generate corresponding VM instructions.
        '''
        structure = self.create_structure(0, len(self.content))
        class_name = content(self.content[structure[1][0]])
        this_class = JackClass(class_name)
        # print(structure)
        for block in structure:
            start = block[0]
            current_token = token(self.content[start])
            if current_token == 'classVarDec':
                self.compile_class_Var_dec(*block, this_class)
            elif current_token == 'subroutineDec':
                self.compile_subroutine_dec(*block, this_class)
        # self.VMcode.append(f'//vars in {this_class.name}: {this_class.vars}\n')
        self.VarTable = this_class.vars

    def create_structure(self, id_s, id_e):
        '''
        Analyzes a segment of parsed code and organizes it into a structure.
        '''
        if id_s == id_e or id_s == id_e - 1:
            return []
        code_segment = self.content[id_s:id_e+1]
        indent = 0
        for char in code_segment[1]:
            if char == " ":
                indent += 1
            else:
                break
        structure = []
        start = 0
        for idx, xml in enumerate(code_segment):
            if idx == 0 or idx == len(code_segment):
                continue
            if indent < len(xml) and xml[indent] != " " and not xml.strip().startswith('</'):
                if idx > 1:
                    structure.append((start, idx - 1))
                start = idx
        structure.append((start, len(code_segment) - 2))
        return structure

    def compile_class_Var_dec(self, ids, ide, this_class):
        '''
        Compiles class-level variable declarations (static or field) into the
        class symbol table.
        '''
        kind = content(self.content[ids+1])
        var_type = content(self.content[ids+2])
        for i in range(3, ide - ids - 1):
            if content(self.content[ids+i]) == ',':
                continue
            var_name = content(self.content[ids+i])
            if kind == "static":
                # self.VMcode.append(f'//static var {var_name} in class {this_class.name}\n')
                this_class.add_static(var_name, var_type)
            else:
                # self.VMcode.append(f'//feild var {var_name} in class {this_class.name}\n')
                this_class.add_field(var_name, var_type)

    def compile_subroutine_dec(self, ids, ide, this_class):
        '''
        Compiles a subroutine declaration and generates its corresponding
        VM code.
        '''
        # print(this_class.vars)
        # self.VMcode.append(f'// subroutine_dec in {this_class}\n')
        structure = self.create_structure(ids, ide)
        # print(structure)
        class_name = this_class.name
        subroutine_type = content(self.content[ids+1])
        # print("s-type is", subroutine_type)
        return_type = content(self.content[ids+2])
        subroutine_name = content(self.content[ids+3])
        this_subroutine = JackSubroutine(
            subroutine_name, subroutine_type, return_type, this_class)
        # print(subroutine_name, subroutine_type, return_type, this_class)

        # parameter_list - add arguments
        p_start = ids + structure[4][0]
        p_end = ids + structure[4][1]
        num_p = 0
        if p_end > p_start + 1:
            num_p = (p_end - p_start) // 3
            for i in range(num_p):
                var_type = content(self.content[p_start+3*i+1])
                var_name = content(self.content[p_start+3*i+2])
                this_subroutine.add_arg(var_name, var_type)
        
        # compile subroutine
        s_start = ids + structure[6][0]
        s_end = ids + structure[6][1]
        subroutine_body = self.create_structure(s_start, s_end)
        num_loc = 0

        # var declaration
        for code_segment in subroutine_body[1:-1]:
            # print(code_segment)
            start = s_start + code_segment[0]
            end = s_start + code_segment[1]
            current_token = token(self.content[start])
            # print(current_token)
            # print(token(self.content[end]))
            if current_token == 'varDec':
                num_loc += self.compile_Var_dec(start, end, this_subroutine)
        # print(this_subroutine.name, f"lcl var: {num_loc}")

        self.VMcode.append(f'function {class_name}.{subroutine_name} {num_loc}\n')
        
        # memory allocation
        if subroutine_type == 'constructor':
            self.VMcode.append(f'push constant {this_class.field_symbols}\n')
            self.VMcode.append('call Memory.alloc 1\n')
            self.VMcode.append('pop pointer 0\n')
        elif subroutine_type == 'method':
            self.VMcode.append('push argument 0\n')
            self.VMcode.append('pop pointer 0\n')
        
        # statements
        for code_segment in subroutine_body[1:-1]:
            # print(code_segment)
            start = s_start + code_segment[0]
            end = s_start + code_segment[1]
            current_token = token(self.content[start])
            # print(current_token)
            # print(token(self.content[end]))
            if current_token == 'statements':
                self.compile_statements(start, end, this_subroutine)
        # self.VMcode.append(f"//current fuction vars: {this_subroutine.vars}\n")

    def compile_Var_dec(self, ids, ide, this_subroutine):
        '''
        Compiles a local variable declaration within a subroutine.
        '''
        var_type = content(self.content[ids+2])
        var_num = 0
        for i in range(3, ide - ids - 1):
            if content(self.content[ids+i]) == ',':
                continue
            var_name = content(self.content[ids+i])
            # self.VMcode.append(f'//var {var_name} in {this_subroutine.subroutine_type} {this_subroutine.name}\n')
            this_subroutine.add_var(var_name, var_type)
            var_num += 1
        return var_num

    def compile_statements(self, ids, ide, this_subroutine):
        '''
        Compiles a statements block within a subroutine.
        '''
        # print(this_subroutine.vars)
        # print("current compiling:\n", '\n'.join(self.content[ids:ide+1]))
        statements = self.create_structure(ids, ide)
        for statement in statements:
            start = ids + statement[0]
            end = ids + statement[1]
            todo = token(self.content[start])
            # print(todo)
            if todo == "letStatement":
                self.compile_let(start, end, this_subroutine)
            elif todo == "ifStatement":
                self.compile_if(start, end, this_subroutine)
            elif todo == "whileStatement":
                self.compile_while(start, end, this_subroutine)
            elif todo == "doStatement":
                self.compile_do(start, end, this_subroutine)
            else:
                self.compile_return(start, end, this_subroutine)

    def compile_let(self, ids, ide, this_subroutine):
        '''
        Compiles a `let` statement.
        '''
        # print("current compiling:\n", '\n'.join(self.content[ids:ide+1]))
        # self.VMcode.append('// let statement\n')
        structure = self.create_structure(ids, ide)
        if len(structure) == 5:         # normal variable or initialize an array
            expression = structure[3]
            start = ids + expression[0]
            end = ids + expression[1]
            self.compile_expression(start, end, this_subroutine)
            variable_name = content(self.content[ids+2])
            try:
                var = this_subroutine.vars[variable_name]
            except KeyError:
                var = this_subroutine.jack_class.vars[variable_name]
            kind = var.kind     # talel value variable
            segment = self.mem_seg[kind]
            offset = var.index     # normal variable
            self.VMcode.append(f"pop {segment} {offset}\n")
        else:                           # array variable
            # 'push offset'
            id_expression = structure[3]
            # print(structure)
            id_ex_start = ids + id_expression[0]
            id_ex_end = ids + id_expression[1]
            # print("offset is:", self.content[id_ex_start:id_ex_end])
            self.compile_expression(id_ex_start, id_ex_end, this_subroutine)

            # 'push {arrayname}'
            variable_name = content(self.content[ids+2])
            try:
                var = this_subroutine.vars[variable_name]
            except KeyError:
                var = this_subroutine.jack_class.vars[variable_name]
            kind = var.kind     # talel value variable
            segment = self.mem_seg[kind]
            offset = var.index     # normal variable
            self.VMcode.append(f"push {segment} {offset}\n")

            self.VMcode.append('add\n')

            # value to assign
            # print('assign to an array')
            expression = structure[6]
            start = ids + expression[0]
            end = ids + expression[1]
            # print("current compiling:\n", '\n'.join(self.content[ids:ide+1]))
            self.compile_expression(start, end, this_subroutine)

            self.VMcode.append('pop temp 0\n')
            self.VMcode.append('pop pointer 1\n')
            self.VMcode.append('push temp 0\n')
            self.VMcode.append('pop that 0\n')
        return

    def compile_if(self, ids, ide, this_subroutine):
        '''
        Compiles an `if` statement.
        '''
        # self.VMcode.append('// if statement\n')
        structure = self.create_structure(ids, ide)
        expression = structure[2]
        e_start = ids + expression[0]
        e_end = ids + expression[1]
        statements = structure[5]
        s_start = ids + statements[0]
        s_end = ids + statements[1]
        # condition
        self.compile_expression(e_start, e_end, this_subroutine)
        self.VMcode.append('not\n')

        global jumplabel
        else_lable = f'ELSELABLE{jumplabel}'
        jumplabel += 1
        end_lable = f'ENDLABLE{jumplabel}'
        jumplabel += 1

        self.VMcode.append(f'if-goto {else_lable}\n')
        # statement
        self.compile_statements(s_start, s_end, this_subroutine)
        # else-statement
        self.VMcode.append(f'goto {end_lable}\n')
        self.VMcode.append(f'label {else_lable}\n')
        if len(structure) > 7:
            else_statements = structure[9]
            start = ids + else_statements[0]
            end = ids + else_statements[1]
            self.compile_statements(start, end, this_subroutine)
        self.VMcode.append(f'label {end_lable}\n')
        # TODO: modyfied 1

    def compile_while(self, ids, ide, this_subroutine):
        '''
        Compiles an `while` statement.
        '''
        # self.VMcode.append('// while statement\n')

        structure = self.create_structure(ids, ide)
        expression = structure[2]
        e_start = ids + expression[0]
        e_end = ids + expression[1]
        statements = structure[5]
        s_start = ids + statements[0]
        s_end = ids + statements[1]
        global jumplabel
        loop_lable = f'WHILELABLE{jumplabel}'
        jumplabel += 1
        end_lable = f'ENDLABLE{jumplabel}'
        jumplabel += 1
        self.VMcode.append(f'label {loop_lable}\n')
        # condition
        self.compile_expression(e_start, e_end, this_subroutine)
        self.VMcode.append('not\n')
        self.VMcode.append(f'if-goto {end_lable}\n')
        # statement
        self.compile_statements(s_start, s_end, this_subroutine)
        self.VMcode.append(f'goto {loop_lable}\n')
        # end
        self.VMcode.append(f'label {end_lable}\n')

    def compile_do(self, ids, ide, this_subroutine):
        '''
        Compiles an `do` statement.
        '''
        # print("compileing dostatement")
        # print("current compiling:\n", '\n'.join(self.content[ids:ide+1]))
        # self.VMcode.append('// do statement\n')
        self.compile_subroutine_call(ids+2, ide-2, this_subroutine)
        self.VMcode.append('pop temp 0\n')  # clear stack to avoid gabage

    def compile_return(self, ids, ide, this_subroutine):
        '''
        Compiles an `return` statement.
        '''
        # self.VMcode.append('// return statement\n')
        structure = self.create_structure(ids, ide)
        if len(structure) == 2:
            self.VMcode.append('push constant 0\n')
        else:
            self.compile_expression(ids+2, ide-2, this_subroutine)
        self.VMcode.append('return\n')

    def compile_expression(self, ids, ide, this_subroutine):
        '''
        Compiles an expression in a Jack program.
        '''
        # print("current compiling:\n", '\n'.join(self.content[ids:ide+1]))
        structure = self.create_structure(ids, ide)
        # print(structure)
        if len(structure) == 0:
            return
        elif len(structure) == 1:      # single term
            start = ids + structure[0][0]
            end = ids + structure[0][1]
            self.compile_term(start, end, this_subroutine)
        else:
            # compile expression1
            start = ids + structure[0][0]
            end = ids + structure[0][1]
            self.compile_term(start, end, this_subroutine)

            # compile expression2
            start = ids + structure[2][0]
            end = ide - 1
            self.compile_term(start, end, this_subroutine)

            # compile oprator
            start = ids + structure[1][0]
            end = ids + structure[1][1]
            self.compile_op(start, end, this_subroutine)

    def compile_op(self, ids, ide, this_subroutine):
        '''
        Compile operators.
        '''
        self.VMcode.append(self.op_dic[content(self.content[ids])])

    def compile_term(self, ids, ide, this_subroutine):
        '''
        Compiles a single term in a Jack expression.
        '''
        # print("current compiling:\n", '\n'.join(self.content[ids:ide+1]))
        structure = self.create_structure(ids, ide)
        current_token = token(self.content[ids+1])
        current_content = content(self.content[ids+1])
        if current_token == 'keyword':              # keyword: true/false/null/this
            if current_content == 'true':
                self.VMcode.append('push constant 0\n')
                self.VMcode.append('not\n')
            elif current_content in ('false', 'null'):
                self.VMcode.append('push constant 0\n')
            else:
                self.VMcode.append('push pointer 0\n')
        elif current_token == 'symbol':             # symbol: (expr)/naryOp
            # unaryOp term
            if current_content in ('-', '~'):
                # compile term
                start = ids + structure[1][0]
                end = ide - 1
                self.compile_term(start, end, this_subroutine)
                # compile op
                self.VMcode.append(self.unaryOp_dic[current_content])
            # (expression)
            else:
                self.compile_expression(ids+2, ide-2, this_subroutine)
        elif current_token == 'integerConstant':    # integer
            self.VMcode.append(f'push constant {current_content}\n')
        elif current_token == 'stringConstant':     # string
            to_write = self.content[ids+1].strip().split("<")[1].split('>')[1][1:-1]
            # print("string is ", to_write)
            len_string = len(to_write)
            # print(f'{to_write=}')
            self.VMcode.append(f'push constant {len_string}\n')
            self.VMcode.append('call String.new 1\n')
            for c in to_write:
                self.VMcode.append(f'push constant {ord(c)}\n')
                self.VMcode.append('call String.appendChar 2\n')
        else:                                       # identifier
            # varname
            if len(structure) == 1:
                variable_name = content(self.content[ids+1])
                try:
                    var = this_subroutine.vars[variable_name]
                except KeyError:
                    var = this_subroutine.jack_class.vars[variable_name]
                kind = var.kind
                segment = self.mem_seg[kind]
                offset = var.index
                self.VMcode.append(f"push {segment} {offset}\n")
            # varname[expression]
            elif content(self.content[ids + 2]) == '[':
                # print("this is array")
                arr = current_content  #
                # print(arr)
                try:
                    var = this_subroutine.vars[arr]
                except KeyError:
                    var = this_subroutine.jack_class.vars[arr]
                kind = var.kind
                segment = self.mem_seg[kind]
                offset = var.index
                # print(var, kind, segment, offset)
                
                # STEP1 calculate id of arr[idx]
                # get idx of array
                e_start = ids + structure[2][0]
                e_end = ids + structure[2][1]
                self.compile_expression(e_start, e_end, this_subroutine)
                # get id of arr
                self.VMcode.append(f"push {segment} {offset}\n")
                # add them together
                self.VMcode.append("add\n")

                # STEP2 read value
                self.VMcode.append("pop pointer 1\n")
                self.VMcode.append("push that 0\n")
            # subroutine call: method from other class
            else:
                self.compile_subroutine_call(ids+1, ide-1, this_subroutine)
        return

    def compile_subroutine_call(self, ids, ide, this_subroutine):
        '''
        Compiles a subroutine call in a Jack program.
        '''
        # print("sub routine current compiling:\n", '\n'.join(self.content[ids:ide+1]))
        # function/constructor from other class // method from an object
        if content(self.content[ids + 1]) == '.':
            # self.VMcode.append("//outer class method\n")
            arg_num = 0
            pre_name = content(self.content[ids + 0])
            if pre_name in this_subroutine.vars:                   # object in lcl
                var = this_subroutine.vars[pre_name]
                pre_name = var.type
                kind = var.kind
                idx = var.index
                segment = self.mem_seg[kind]
                self.VMcode.append(f'push {segment} {idx}\n')
                arg_num += 1
                # print(pre_name, kind, idx, f'{arg_num=}')
            elif pre_name in this_subroutine.jack_class.vars:      # object in field
                var = this_subroutine.jack_class.vars[pre_name]
                pre_name = var.type
                kind = var.kind
                idx = var.index
                segment = self.mem_seg[kind]
                self.VMcode.append(f'push {segment} {idx}\n')
                arg_num += 1
                # print(pre_name, kind, idx, f'{arg_num=}')
            arg_num += self.compile_expression_list(ids + 4, ide - 1, this_subroutine)
            func_name = pre_name
            func_name += content(self.content[ids + 1])
            func_name += content(self.content[ids + 2])
            self.VMcode.append(f'call {func_name} {arg_num}\n')
        # function/method from this class
        else:
            # self.VMcode.append("//function or class method\n")
            to_call = content(self.content[ids + 0])

            arg_num = 0
            arg_num += 1
            self.VMcode.append('push pointer 0\n')

            arg_num += self.compile_expression_list(ids + 2, ide - 1, this_subroutine)
            func_name = this_subroutine.jack_class.name
            func_name += '.'
            func_name += to_call
            self.VMcode.append(f'call {func_name} {arg_num}\n')

    def compile_expression_list(self, ids, ide, this_subroutine):
        '''
        Compiles a list of expressions provided as arguments to a
        subroutine call.
        '''
        # print("current compiling:\n", '\n'.join(self.content[ids:ide+1]))
        expression_list = self.create_structure(ids, ide)
        num_arg = 0
        for start, end in expression_list:
            if token(self.content[ids+start]) == 'expression':
                num_arg += 1
                self.compile_expression(ids+start, ids+end, this_subroutine)
        return num_arg

    def __repr__(self):
        return f'structure with {len(self.structure)} components.'


def token(xml: str):
    '''
    Extracts the XML token type from a given XML line.
    '''
    return xml.split('>')[0].split('<')[-1]


def content(xml: str):
    '''
    Extracts the content (value) of a given XML line.
    '''
    return xml.strip().split('<')[1].split(' ')[-2]

###########################################################################
###########################################################################

if __name__ == "__main__":
    main()
