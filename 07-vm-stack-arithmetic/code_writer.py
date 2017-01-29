#!/usr/bin/env python
"""The CodeWriter Module

Translates VM commands into Hack assembly code.
EXPORTED CLASSES: ArithmeticCommands, CodeWriter

"""
import os
import re


class ArithmeticCommands:
    """Manages symbol translations/equivalents for the nine Arithmetic and Logical commands.

    Symbols are stored in dictionaries within a dictionary (as key-val pairs based on command type)

    """
    _COMMANDS_SYMBOLS = {
        'binary_compute': {
            'add': '+',
            'sub': '-',
            'and': '&',
            'or': '|',
            },

        'unary_compute': {
            'not': '!',
            'neg': '-',
            },

        'binary_logic': {
            'eq': 'JEQ',
            'gt': 'JGT',
            'lt': 'JLT',
            }
        }

    @classmethod
    def all_commands(cls):
        """Returns all the arithmetic commands."""
        commands = []
        for type in cls._COMMANDS_SYMBOLS:
            for cmd in cls._COMMANDS_SYMBOLS[type]:
                commands.append(cmd)
        return commands

    @classmethod
    def types(cls):
        """Returns all the arithmetic command types."""
        return cls._COMMANDS_SYMBOLS.keys()

    @classmethod
    def type_commands(cls, type):
        """Returns all the arithmetic commands associated with a specific type."""
        return cls._COMMANDS_SYMBOLS[type]

    @classmethod
    def symbol(cls, type, command):
        """Returns the symbol of a specific arithmetic/logical command."""
        return cls._COMMANDS_SYMBOLS[type][command]



class CodeWriter:
    """Generates HACK assembly code from VM commands into a corresponding output file."""
    
    # CONSTANT and STATIC segments handled as special case
    _VM_SEGMENTS = {
        # for each instance of running function
        'instance': {
            'local': 'LCL',
            'argument': 'ARG',
            'this': 'THIS',
            'that': 'THAT',
            },

        # shared by all functions in program
        'shared': {
            'pointer': 'THIS',
            'temp': 'R5'
            }
        }

    def __init__(self, vm_file):
        """Opens the output file/stream and gets ready to write into it."""
        self._output_file = open(self._get_filename(vm_file), 'w')
        self._label_count = 0

    def _get_filename(self, vm_file):
        """Checks whether .vm file or .asm file.
        
        Arguments: vm_file -- .vm file (string)
        Returns: .vm file with .asm extension

        """
        asm_extension = '.asm'
        filename = re.compile(r'\.vm$', re.IGNORECASE).sub(asm_extension, vm_file)
        if not filename.endswith(asm_extension):
            filename += asm_extension
        return filename

    def set_filename(self, vm_file):
        """Informs the code writer that the translation of a new VM file is started.
        
        Arguments:
        vm_file -- filename (string)

        """
        vm_file = os.path.basename(vm_file)
        self._vm_basename = re.compile(r'\.vm$', re.IGNORECASE).sub('', vm_file)
        
    def _write(self, str):
        # Writes string to output file (general)
        self._output_file.write(str + '\n')

    def _write_comment(self, comment):
        # Write comment to output file
        self._write('// %s' %comment)

    def _write_instruction(self, commands):
        # Writes instructions (list of commands) to output file w/ each command on newline
        # Indents command unless label
        commands = [[4*' ', ''][cmd.startswith('(')] + cmd for cmd in commands]
        self._write('\n'.join(commands))

    def write_arithmetic(self, command):
        """Writes the assembly code that is the translation of the given arithmetic command.

        Arguments:
        command -- the arithmetic command to translate and write to output file (string)

        """
        for type in ArithmeticCommands.types():
            if command in ArithmeticCommands.type_commands(type):
                self._write_comment(command)
                # Determine which type of arithmetic command to write, then calls corresponding method
                write_method = getattr(self, '_write_%s' %type)
                write_method(ArithmeticCommands.symbol(type, command))
                self._write('')    # write newline
                break
        else:
            raise CodeWriterError("Unknown Arithmetic or Logical Command: %s" %command)
        
    def _write_binary_compute(self, symbol):
        '''Writes the assembly code to compute a binary function (add, sub, and, or).
        
        Arguments: symbol -- corresponding operation symbol for the command (string)

        '''
        self._pop_from_stack_to('D')
        self._pop_from_stack_to('A')
        self._write_instruction(['D=A%sD' %symbol]);
        self._push_to_stack_from('D')

    def _write_unary_compute(self, symbol):
        """Writes the assembly code to compute a unary function (neg, not).

        Arguments: symbol -- corresponding operation symbol for the command (string)

        """
        self._write_instruction(['@SP', 'A=M-1', 'M=%sM' %symbol])

    def _write_binary_logic(self, symbol):
        """Writes the assembly code to compute a binary function that returns a Boolean (eq, gt, lt).
        
        Arguments: symbol -- corresponding opration symbol for the command (string)
        
        """
        # Increment count for unique labels
        self._label_count += 1
        label = 'LABEL%d' %self._label_count

        self._pop_from_stack_to('D')
        self._pop_from_stack_to('A')
        self._write_instruction(['D=A-D'])
        self._write_instruction(['@%s_TRUE' %label, 'D;%s' %symbol])
        self._push_boolean_to_stack(False)
        self._write_instruction(['@%s_FALSE' %label, '0;JMP', '(%s_TRUE)' %label])
        self._push_boolean_to_stack(True)
        self._write_instruction(['(%s_FALSE)' %label])
        
    def _pop_from_stack_to(self, register):
        """Writes the assembly code for storing a value form RAM to register.
        
        Arguments: register -- the register to store the value (string)

        """
        self._write_instruction(['@SP', 'AM=M-1', '%s=M' %register])

    def _push_to_stack_from(self, register):
        """Writes the assembly code for storing a value from the register to RAM.

        Arguments: register -- the register to retrieve the value from to store into RAM (string)

        """
        self._write_instruction(['@SP', 'M=M+1', 'A=M-1', 'M=%s' %register])
    
    def _push_boolean_to_stack(self, boolean):
        '''Writes the assembly code for storing a boolean value to RAM.
        
        Arguments: boolean -- the boolean value to store into RAM

        '''

        self._write_instruction(['@SP', 'M=M+1', 'A=M-1', 'M=%d' %(0, -1)[boolean]])

    def write_push_pop(self, command, segment, index):
        """Writes the assembly code that is the translation of the given C_PUSH or C_POP command.

        Arguments:
        command -- 'C_PUSH' or 'C_POP'
        segment -- name of virtual memory segment (string)
        index -- nonnegative decimal that specifies location within memory segment (int)

        """
        # Join command with arguments
        full_command = ' '.join((command, segment, index))
        self._write_comment(full_command)

        if command == 'push' and segment == 'constant':
            self._push_constant(index)
        elif segment in self._VM_SEGMENTS['shared'].keys() + self._VM_SEGMENTS['instance'].keys():
            self._push_pop_variable(command, segment, index)
        elif segment == 'static':
            self._push_pop_static(command, index)
        else:
            raise CodeWriterError("Unknown Push/Pop Command: %s" %full_command)
        
        self._write('')    # write newline

    def _push_constant(self, constant):
        """Writes the assembly code that corresponds to pushing a constant to the stack. 

        Constant stored in virtual CONSTANT segment.
        Arguments: constant -- the value to push to stack

        """
        self._write_instruction(['@%s' %constant, 'D=A', '@SP', 'M=M+1', 'A=M-1', 'M=D'])
        
    def _push_pop_variable(self, command, segment, index):
        """Writes the assembly code that corresponds to push/pop variable to/from the specified vm segment.

        Arguments:
        command -- either 'push' or 'pop' command (string)
        segment -- the specified memory segment to be accessed (string)
        index -- the offset from the base address (integer)

        """
        if command == 'push':
            self._get_address('A', segment, index)
            self._write_instruction(['D=M'])
            self._push_to_stack_from('D')
        elif command == 'pop':
            self._get_address('D', segment, index)
            self._write_instruction(['@R13', 'M=D'])
            self._pop_from_stack_to('D')
            self._write_instruction(['@R13', 'A=M', 'M=D'])
        else:
            raise CodeWriterError("Unknown Command (Not Push/Pop): %s" %command)

    def _get_address(self, register, segment, index):
        """Calculates the address and writes the necessary assembly code.
        
        Resulting address = segment[index] or base address + index
        Arguments:
        register -- the register to store the resulting address (string)
        segment -- the segment to be accessed for calculating base address (string)
        index -- the offset from base address (location within segment) (integer)

        """
        if segment in self._VM_SEGMENTS['instance']:
            base_addr = self._VM_SEGMENTS['instance'][segment]
            loc = 'M'
        elif segment in self._VM_SEGMENTS['shared']:
            base_addr = self._VM_SEGMENTS['shared'][segment]
            loc = 'A'

        self._write_instruction(['@%s' %index, 'D=A', '@%s' %base_addr, '%s=%s+D' %(register, loc)])

    def _push_pop_static(self, command, var):
        """Writes the assembly code that corresponds to push/pop static variables to STATIC vm segment.

        Arguments:
        command -- the memory access command, either 'push' or 'pop' (string)
        var -- the satic variable symbol extension (Xxx.var)

        """
        symbol = '%s.%s' %(self._vm_basename, var)
        if command == 'push':
            self._write_instruction(['@%s' %symbol, 'D=M'])
            self._push_to_stack_from('D')
        elif command == 'pop':
            self._pop_from_stack_to('D')
            self._write_instruction(['@%s' %symbol, 'M=D'])
        else:
            raise CodeWriterError("Unknown Command (Not Push/Pop): %s" %command)
            
    def close(self):
        """Writes the assembly code to end a program, using infinite loop, and closes the output file."""
        self._write_comment("Infinite Loop (Terminator)")
        self._write_instruction(['(END)', '@END', '0;JMP'])
        self._output_file.close()
        

class CodeWriterError(Exception):
    """For code translation/writing error exceptions; null operation -- nothing happens."""
    pass

