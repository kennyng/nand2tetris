#!/usr/bin/env python
"""The VMWriter Module.

Emits VM commands into a file using the VM command syntax.
EXPORTED CLASS: VMWriter

"""
import os
from symbol_table import SymbolTable

class VMWriter:
    
    @staticmethod
    def write_push(segment, index):
        """Writes a VM push command.

        Arguments: 
        segment -- 'CONST' | 'ARG' | 'LOCAL' | 'STATIC' | 'THIS' | 'THAT' | 'POINTER' | 'TEMP'
        index (int)

        """
        return ['push %s %d' %(segment, index)]

    @staticmethod
    def write_pop(segment, index):
        """Writes a VM pop command.

        Arguments: 
        segment -- 'CONST' | 'ARG' | 'LOCAL' | 'STATIC' | 'THIS' | 'THAT' | 'POINTER' | 'TEMP'
        index (int)

        """
        return ['pop %s %d' %(segment, index)]

    @staticmethod
    def write_arithmetic(command):
        """Writes a VM arithmetic command.

        Argument:
        command -- 'ADD' | 'SUB' | 'NEG' | 'EQ' | 'GT' | 'LT' | 'AND' | 'OR' | 'NOT'

        """
        return [command]

    @staticmethod
    def write_label(label):
        """Writes a VM label command.

        Argument: label (string)

        """
        return ['label %s' %label]
    
    @staticmethod
    def write_goto(label):
        """Writes a VM goto command.

        Argument: label (string)

        """
        return ['goto %s' %label]
        
    @staticmethod
    def write_if(label):
        """Writes a VM if-goto command.

        Argument: label (string)

        """
        return ['if-goto %s' %label]

    @staticmethod
    def write_call(name, n_args):
        """Writes a VM call command.

        Arguments:
        name (string)
        n_args -- number of arguments (int)

        """
        return ['call %s %d' %(name, n_args)]

    @staticmethod
    def write_function(name, n_locals):
        """Writes a VM function command.

        Arguments:
        name (string)
        n_locals -- number of local variables (int)

        """
        return ['function %s %d' %(name, n_locals)]

    @staticmethod
    def write_return():
        """Writes a VM return command."""
        return ['return']


