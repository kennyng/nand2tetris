#!/usr/bin/env python
"""The Parser Module.

Handles the parsing if a single .vm file, and encapsulates access to the input code.
EXPORTED CLASSES: Parser

"""
from code_writer import ArithmeticCommands


class Parser:
    """Reads VM commands, parses them, and provides convenient access to their components."""

    def __init__(self, filename):
        """Opens input file/stream and gets ready to parse it.
        
        Arguments: filename -- input file/stream
        
        """
        self._file = open(filename)
        # must init (read) next command for has_more_commands() to function correctly
        # since advance() has not been called yet and initially there is no current command
        self._read_next_command()

    def close(self):
        """Closes the input file/stream."""
        self._file.close()

    def has_more_commands(self):
        """Checks if there are more commands in input file. Returns: boolean"""
        return self._next_command != None

    def advance(self):
        """Reads next command from the input and makes it the current command. 
        
        Should be called only if has_more_commands() is true.
        Each command is parsed into three tokens (command arg1 arg2) and stored
   
        """
        self._parse_command(self._next_command)
        self._read_next_command()

    def _parse_command(self, command):
        """Splits full instruction into three tokens [command arg1 arg2]

        Arguments: command -- the full command to parse (string)

        """
        tokens = command.split()
        tokens = [str.lower() for str in tokens]
        # If < 2 arguments, use empty object ensure at least 3 objects in tokens
        tokens.extend([None, None])
        self._command, self._arg1, self._arg2 = tokens[:3]

    def _read_next_command(self):
        '''Reads next command from input, and in doing so, removes whitespace and comments.'''
        while True:
            command = self._file.readline()
            # Check EOF
            if not command:
                self._next_command = None
                break
            # Remove comments and extra whitespace from line if present
            command = command[:command.find('//')].strip()
            # Read line until non-whitespace found
            if command:
                self._next_command = command
                break
    
    def command_type(self):
        """Returns the type of the current VM command.
        
        C_ARITHMETICS is returned for all the arithmetic commands.

        """
        types = {'push': 'C_PUSH', 'pop': 'C_POP'}
        # Add all arithmetic and logical commands to types dict 
        for command in ArithmeticCommands.all_commands():
            types[command] = 'C_ARITHMETIC'

        if self._command in types:
            return types[self._command]
        raise ParserError('Unknown commandL %s' %self._command)

    def arg1(self):
        """Returns the first argument of the current command.

        In the case of C_ARITHMETIC, the command itself (add, sub, etc.) is returned.

        """
        if not self._arg1:
            raise ParserError('Missing first argument for %s command.' %self.command_type())
        return self._arg1

    def arg2(self):
        """Returns the second argument of the current command.
        
        Should be called only if the current command is C_PUSH, C_POP.

        """
        if not self.arg2:
            raise ParserError('Missing second argument for &s command.' %self.command_type())
        return self._arg2

    def command(self):
        """Returns the current command."""
        return self._command


class ParserError(Exception):
    """For parsing error exceptions; null operation -- nothing happens.""" 
    pass

