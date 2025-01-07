'''
This module translates arithmetic, logical, and control flow commands from VM
(Virtual Machine) language into Hack Assembly language for the Hack machine
architecture, including flow controling and functions.
'''


num_return_address = 0


def trans_flow(code: list[str]):
    '''
    Translates flow control commands (label, goto, if-goto) to Hack assembly.
    '''
    if code[0] == "label":
        return f'({code[1]})\n'
    elif code[0] == "goto":
        return f'@{code[1]}\n0;JMP\n'
    else:
        return f'@SP\nAM=M-1\nD=M\n@{code[1]}\nD;JNE\n'


def trans_func(code: list[str]):
    '''
    Translates function definition, function call, and function return commands
    into Hack Assembly code.
    '''
    if code[0] == "function":
        func_name = code[1]
        n_locals = int(code[2])
        function_code = f"({func_name})\n"
        for _ in range(n_locals):
            function_code += (
                '@0\n'
                'D=A\n'
                '@SP\n'
                'A=M\n'
                'M=D\n'
                '@SP\n'
                'M=M+1\n'
            )
        return function_code

    elif code[0] == "call":
        push = '@SP\nAM=M+1\nA=A-1\nM=D\n'
        global num_return_address
        num_return_address += 1
        return_label = f"_return_address{num_return_address}"
        return (f'@{return_label}\nD=A\n' + push +
                '@LCL\nD=M\n' + push +
                '@ARG\nD=M\n' + push +
                '@THIS\nD=M\n' + push +
                '@THAT\nD=M\n' + push +
                f'@SP\nD=M\n@{int(code[2])+5}\nD=D-A\n@ARG\nM=D\n' +
                '@SP\nD=M\n@LCL\nM=D\n' +
                f'@{code[1]}\n0;JMP\n' +
                f'({return_label})\n')

    elif code[0] == "return":
        return ('@LCL\nD=M\n@FRAME\nM=D\n' +
                '@5\nA=D-A\nD=M\n@RET\nM=D\n' +
                '@SP\nAM=M-1\nD=M\n@ARG\nA=M\nM=D\n' +
                '@ARG\nD=M+1\n@SP\nM=D\n' +
                '@FRAME\nAM=M-1\nD=M\n@THAT\nM=D\n' +
                '@FRAME\nAM=M-1\nD=M\n@THIS\nM=D\n' +
                '@FRAME\nAM=M-1\nD=M\n@ARG\nM=D\n' +
                '@FRAME\nAM=M-1\nD=M\n@LCL\nM=D\n' +
                '@RET\nA=M\n0;JMP\n')
