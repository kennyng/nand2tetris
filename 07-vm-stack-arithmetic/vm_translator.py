#!/usr/bin/env python
"""VM Translator (main)

Constructs a Parser to parse the VM input file and a CodeWriter to generate code into the correpsonding output file. It goes through the VM commands in the input file and generates Hack assembly code for each command.

"""
import os
import sys
from parser import Parser
from code_writer import ArithmeticCommands
from code_writer import CodeWriter


class VMTranslator:
    def __init__(self, path):
        """Constructs Parser and CodeWriter to translate to assembly code.

        Arguments: path -- the filepath to .vm file or to directory (string)
        
        """
        # Finds all .vm files
        vm_files = self._get_vm_files(path)
        self._code_writer = CodeWriter(path)
        for vm_file in vm_files:
            self._parse_vm_file(vm_file)
        self._code_writer.close()

    def _get_vm_files(self, path):
        """Checks whether directory (containing .vm files?) or file and gets all .vm files.
        
        Arguments: path -- the filepath to .vm file or to directory (string)
        Returns: vm_files -- a list of .vm files (list)

        """
        if os.path.isdir(path):
            vm_files = [os.path.join(path, f) for f in os.listdir(path) if f.lower().endswith('.vm')]
            if len(vm_files) == 0:
                raise IOError("No .vm files in directory: %s" %path)
        elif os.path.isfile(path):
            vm_files = [path]
        else:
            raise IOError("%s is not a file or directory." %path)

        return vm_files

    def _parse_vm_file(self, vm_file):
        '''Creates a Parser to parse each .vm file.
        
        Arguments: vm_file -- the .vm file to parse (string)

        '''
        parser = Parser(vm_file)
        self._code_writer.set_filename(vm_file)

        while parser.has_more_commands():
            parser.advance()
            if parser.command_type() == 'C_ARITHMETIC':
                self._code_writer.write_arithmetic(parser.command())
            elif parser.command_type() in ('C_PUSH', 'C_POP'):
                self._code_writer.write_push_pop(parser.command(), parser.arg1(), parser.arg2())
        parser.close()


# Main
if __name__ == '__main__':
    VMTranslator(sys.argv[1])

