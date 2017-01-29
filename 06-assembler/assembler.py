'''
The Assembler translates programs written in Hack assembly language into the binary code understood by the Hack hardware platform.
It parses the assembly program in two passes. In the first pass, the symbol table is initialized and L_COMMAND labels are added to the symbol table. For the second pass, it goes through the entire program,parsing each line and translating the instructions as well as adding the variables it encounters into the symbol table.

To run: python assembler.py prog.asm

'''


import re
import sys
from os import path
from parser import Parser
from code import Code
from symbol_table import SymbolTable
from symbol_table import SymbolTableBuilder


class Assembler:
    # words are 16 bits long
    _WORD_SIZE = 16

    def __init__(self, filename):
        self._parser = Parser(filename)
        self._symbol_table = SymbolTableBuilder(self._parser).build()
        self._parser.reset()

        self._assembler = open(self._get_filename(filename), 'w')
        self._assemble()

        self._parser.close()
        self._assembler.close()

    # checks whether .asm file or .hack file 
    def _get_filename(self, asm_filename):
        hack_extension = '.hack'
        filename = re.compile(r'\.asm$', re.IGNORECASE).sub(hack_extension, asm_filename)
        if not filename.endswith(hack_extension):
            filename += hack_extension
        return filename

    # Goes through each line in the program and translaes from Hack assembly to binary
    def _assemble(self):
        while self._parser.has_more_commands():
            self._parser.advance()
            command_type = self._parser.command_type()
            if command_type == 'L_COMMAND':
                continue

            command = {'A_COMMAND': self._build_a_command, 'C_COMMAND': self._build_c_command,}[command_type]()
            self._assembler.write(command + '\n')
    
    # Checks whether constant or symbol before tranlating
    def _build_a_command(self):
        symbol = self._parser.symbol()
        if symbol.isdigit():
            return self._get_a_constant(symbol)
        else:
            return self._get_a_address(symbol)

    def _get_a_constant(self, constant):
        max_size = self._WORD_SIZE - 1
        binary = self._convert_decimal_to_binary(constant)
        if len(binary) > max_size:
            raise AssemblerError('Constant %s is too large. Only %s bits available' %(constant, max_size))
        # Pad with leading zeroes
        return '0%s%s' %('0'*(max_size - len(binary)), binary)

    def _convert_decimal_to_binary(self, num):
        binary = ''
        num = int(num)
        while True:
            binary = '%s%s' %(num % 2, binary)
            num /= 2
            if num == 0:
                return binary

    # Checks whether symbol is in symbol table and then retrieves corresponding address
    def _get_a_address(self, symbol):
        if not self._symbol_table.contains(symbol):
            self._symbol_table.add_variable(symbol)
        address = self._symbol_table.get_address(symbol)
        return self._get_a_constant(address)

    # Looks up the mnemonics for its corresponding binary
    def _build_c_command(self):
        return '%s%s%s%s' %('111', Code.comp(self._parser.comp()), Code.dest(self._parser.dest()), Code.jump(self._parser.jump()),)


# For assembler error, raises excepton, does nothing; just for convention
class AssemblerError(Exception):
    pass


# Main: runs the Assembler program in terminal or other shell alternative
if __name__ == '__main__':
    Assembler(sys.argv[1])


