#!/usr/bin/env python
"""The CodeWriter Module

Translates VM commands into Hack assembly code.
EXPORTED CLASSES: CodeWriter

"""
import os
import re
from parser import ArithmeticCommands



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

    def __init__(self, vm_path):
        """Opens the output file/stream and gets ready to write into it."""
        self._output_file = open(self._get_filename_and_path(vm_path), 'w')
        self._label_count = 0
        self._current_function = 'FUNCTION_NAME'
        self.write_init()

    def _get_filename_and_path(self, vm_path):
        """Determines the name/path of the .asm output file given path either to .vm file or to directory of .vm files.
        
        Arguments: vm_path -- the file path of the directory/.vm file(s) (string)
        Returns: a single .asm file located in the same directory as the .vm file(s)

        """
        # Normalize pathname. Condense and remove trailing slash in path (if present)
        vm_path = os.path.normpath(vm_path)
        # Get absolute path
        vm_path = os.path.realpath(vm_path)
        vm_basename = os.path.basename(vm_path)

        # Replace .vm extension with .asm extension; otherwise just append .asm
        asm_extension = '.asm'
        filename = re.compile(r'\.vm$', re.IGNORECASE).sub(asm_extension, vm_basename)
        if not filename.endswith(asm_extension):
            filename += asm_extension

        # Place .asm output file in same directory as .vm file(s)
        if os.path.isdir(vm_path):
            return os.path.join(vm_path, filename)
        else:
            return os.path.join(os.path.dirname(vm_path), filename)

    def set_filename(self, vm_file):
        """Informs the code writer that the translation of new VM file(s) is started.
        
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
            
    def _get_label_symbol(self, label):
        """Generates globally unique symbol in the following format: 'f$b'.

        'f' is the function name and 'b' is the label symbol within the VM function's code.
        Arguments: label -- the label symbol within the VM function's code(string)
        Return: unique symbol in form: 'f$b' (string)

        """
        return '%s$%s' %(self._current_function, label.upper())

    def write_label(self, label):
        """Writes assembly code that effects the 'label' command.

        Arguments: label -- the label symbol within VM function's code (string)

        """
        self._write_instruction(['(%s)' %self._get_label_symbol(label)])

    def write_goto(self, label):
        """Writes assembly code that effects the 'goto' command.

        Arguments: label -- the label symbol within VM function's code (string)

        """
        # extra space to write new line
        self._write_instruction(['@%s' %self._get_label_symbol(label), '0;JMP', ' '])
        
    def write_if(self, label):
        """Writes assembly code that effects the 'if-goto' command.

        Arguments: label -- the label symbol within VM function's code (string)

        """
        self._pop_from_stack_to('D')
        # extra space to write new line
        self._write_instruction(['@%s' %self._get_label_symbol(label), 'D;JNE', ' '])

    def write_call(self, function_name, num_args):
        """Writes assembly code that effects the 'call' command.

        VM command: call 'function_name' 'num_args'
        Calling a function 'function_name' after 'num_args' arguments have been pushed onto the stack.
        
        Arguments:
        function_name -- the name of the function (string)
        num_args -- the number of arguments the function takes (int)
        
        """
        # Increment count for unique labels
        self._label_count += 1
        # for uppercase labels
        function_label = function_name.upper()
        return_address = 'RET_%s_%d' %(function_label, self._label_count)
        
        # push return-address (using declared label)
        self._write_instruction(['@%s' %return_address, 'D=A'])
        self._push_to_stack_from('D')

        # push LCL, ARG, THIS, THAT (save for calling function)
        for address in ('LCL', 'ARG', 'THIS', 'THAT'):
            self._write_instruction(['@%s' %address, 'D=M'])
            self._push_to_stack_from('D')

        # Resposition ARG: ARG = SP - (num_args + 5)
        # D = num_args + 5
        self._write_instruction(['@%s' %num_args, 'D=A', '@5', 'D=A+D'])
        # ARG = SP - D
        self._write_instruction(['@SP', 'D=M-D', '@ARG', 'M=D'])
        
        # LCL = SP
        self._write_instruction(['@SP', 'D=M', '@LCL', 'M=D'])

        # goto function_name (transer control)
        self._write_instruction(['@%s' %function_label, '0;JMP'])
        
        # (return-address) declares label for return-address
        self._write_instruction(['(%s)' %return_address])
    
    def write_function(self, function_name, num_locals):
        """Writes assembly code that effects the 'return' command.

        VM command: function 'function_name' 'num_locals'
        Declaring a function 'function_name' that has 'num_locals' local variables.
        
        Arguments:
        function_name -- the name of the function (string)
        num_locals -- the number of local variables declared within the function (int)

        """
        # for uppercase labels
        function_label = function_name.upper()
        self._current_function = function_label

        lcl_start = '%s_LCL_START' %function_label
        lcl_end = '%s_LCL_END' %function_label

        # Declare a label for the function entry
        self._write_instruction(['(%s)' %function_label])
        # *R13 = num_locals
        self._write_instruction(['@%s' %num_locals, 'D=A', '@R13', 'M=D'])
        # Initialize all local variables (num_locals of them) to 0
        # while( --(*R13) >= 0 )
        self._write_instruction(['(%s)' %lcl_start, '@R13', 'MD=M-1', '@%s' %lcl_end, 'D;JLT'])
        # push constant 0
        self._write_instruction(['@SP', 'M=M+1', 'A=M-1', 'M=0'])
        self._write_instruction(['@%s' %lcl_start, '0;JMP', '(%s)' %lcl_end])

    def write_return(self):
        """Writes the assembly code that effects the 'return' command.

        """
        # FRAME = LCL (FRAME is a temporary variable)
        # Put the return-address in a temp. var.
        # RET = R14 = *(FRAME - 5)
        self._write_instruction(['@5', 'D=A', '@LCL', 'A=M-D', 'D=M', '@R14', 'M=D'])

        # Reposition the return value for the caller at beginning of called function's frame
        # *ARG = pop()
        self._pop_from_stack_to('D')
        self._write_instruction(['@ARG', 'A=M', 'M=D'])

        # Restore SP of the caller so it points to location right after return address of called function
        # SP = ARG + 1
        self._write_instruction(['@ARG', 'D=M+1', '@SP', 'M=D'])

        # Restore THAT, THIS ARG, and LCL of the caller
        # THAT = *(FRAME - 1); THIS = *(FRAME - 2); ARG = *(FRAME - 3); LCL = *(FRAME - 4)
        # *R13 = *LCL
        self._write_instruction(['@LCL', 'D=M', '@R13', 'M=D'])
        # * address = M[--(*R13)]
        for address in ('THAT', 'THIS', 'ARG', 'LCL'):
            self._write_instruction(['@R13', 'AM=M-1', 'D=M', '@%s' %address, 'M=D'])
        
        # goto RET [Goto return-address (in the caller's code)]
        self._write_instruction(['@R14', 'A=M', '0;JMP'])

    def write_init(self):
        """Writes assembly code that effects the VM initialization, also called bootstrap code.

        This code must be placed at the beginning of the output file.
        
        """
        self._write_comment("Initialize SP")
        # Initialize the stack pointet to 256 (0x0100)
        self._write_instruction(['@256', 'D=A', '@SP', 'M=D'])
        # Start executing (the translated code of) Sys.init
        self.write_call('Sys.init', 0)

    def close(self):
        """Writes the assembly code to end a program, using infinite loop, and closes the output file."""
        self._write_comment("Infinite Loop (Terminator)")
        self._write_instruction(['(END)', '@END', '0;JMP'])
        self._output_file.close()
        

class CodeWriterError(Exception):
    """For code translation/writing error exceptions; null operation -- nothing happens."""
    pass

