#!/usr/bin/env python
"""VM Translator (main)

Constructs a Parser to parse the VM input file and a CodeWriter to generate code into the correpsonding output file. 
It goes through the VM commands in the input file and generates Hack assembly code for each command.
If the program's argument is a directory rather than a filename, the main program will process all the .vm files
in this directory. In doing so, it uses a separate Parser for handling each input file and a single CodeWriter for handling
the output.

"""
import os
import sys
from parser import Parser
from parser import ArithmeticCommands
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
            type = parser.command_type()

            if type == 'C_ARITHMETIC':
                self._code_writer.write_arithmetic(parser.command())
            elif type in ('C_PUSH', 'C_POP'):
                self._code_writer.write_push_pop(parser.command(), parser.arg1(), parser.arg2())
            elif type == 'C_LABEL':
                self._code_writer.write_label(parser.arg1())
            elif type == 'C_GOTO':
                self._code_writer.write_goto(parser.arg1())
            elif type == 'C_IF':
                self._code_writer.write_if(parser.arg1())
            elif type == 'C_CALL':
                self._code_writer.write_call(parser.arg1(), parser.arg2())
            elif type == 'C_FUNCTION':
                self._code_writer.write_function(parser.arg1(), parser.arg2())
            elif type == 'C_RETURN':
                self._code_writer.write_return()

        parser.close()


# Main
if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit('Usage: %s [.vm file or directory containing .vm files]' %sys.argv[0])
    VMTranslator(sys.argv[1])

