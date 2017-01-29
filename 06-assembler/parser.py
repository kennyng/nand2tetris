'''
The Parser module reads and assembly language comand, parses it, and provides convenient access to the command's components (fields and symbols). In addtion, it removes all white space and comments.

'''

import re
from code import Code
from code import Translate


class Parser:
    # Opens input file/stream and gets ready to parse it
    def __init__(self, filename):
        self._file = open(filename)
        self.reset()

    # closes input file/stream
    def close(self):
        self._file.close()

    # Rewinds input file/stream to beginning for second pass/read
    def reset(self):
        self._file.seek(0)
        # must init (read) next command for has_more_commands() to function correctly
        # since advance() has not been called yet and initially tere is no current command
        self._read_next_command()

    # Checks if more commands in input file 
    def has_more_commands(self):
        return self._next_command != None

    # Reads next command from the input and makes it the current command. Should be called only
    # if has_more_commands() returns true. Initially, no current commands.
    # The current command and next command are stored in order to determine whether a valid command
    # follows the current one.
    def advance(self):
        self._command = self._next_command
        self._read_next_command()

    # Reads next command from input, in doing so removes whitespace and comments
    def _read_next_command(self):
        while True:
            command = self._file.readline()
            # check EOF
            if not command:
                self._next_command = None
                break
            # Remove comments and extra whitespace from line if present
            command = command[:command.find('//')].strip()
            # Read line until non-whitespace found
            if command:
                self._next_command = command
                break

    # Returns type of current command
    def command_type(self):
        if self._command.startswith('@'):
            return 'A_COMMAND'
        elif self._command.startswith('('):
            return 'L_COMMAND'
        else:
            return 'C_COMMAND'

    # Returns the symbol or constant Xxx of the current command @Xxx or (Xxx)
    def symbol(self):
        return re.search(r'[(@]([a-zA-Z0-9_.$:]+)\)?', self._command).group(1)

    # Returns dest mnemonic in current C-Instruction
    def dest(self):
        return self._parse_mnemonic('dest')

    # Returns comp mnemonic in current C-Instruction
    def comp(self):
        return self._parse_mnemonic('comp')

    # Returns jump mnemonic in current C-Instruction
    def jump(self):
        return self._parse_mnemonic('jump')

    # Returns only the field type from the C-Instruction that is specified
    def _parse_mnemonic(self, type):
        fields = self._split_c_instruction()
        if fields[type] not in Translate.CODES[type]:
            raise ParserError('Invalid %s: %s' %(type, fields[type]))
        return fields[type]

    # Splits the 3 different field types and stores into dictionary for retrieval
    def _split_c_instruction(self):
        fields = self._command.split('=', 1)
        if len(fields) > 1:
            dest, comp = fields
        else:
            dest, comp = None, fields[0]

        fields = comp.split(';', 1)
        if len(fields) > 1:
            comp, jump = fields
        else:
            comp, jump = fields[0], None
        
        return {'dest': dest, 'comp': comp, 'jump': jump}


# For parsing error exceptions; does nothing, meant for convention
class ParserError(Exception):
    pass


