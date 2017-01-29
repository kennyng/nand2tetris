#!/usr/bin/env python
"""The JackCompiler Module.

The compiler program operates on a given source, where source is either a filename of the form Xxx.jack 
or a directory name containing on or more .jack files. For each source Xxx.jack, the analyzer goes through
the following logic:
1. Create a JackTokenizer from the Xxx.jack input file.
2. Create a SyntaxAnalyzer to parse the list of tokens.
3. Create an output file called Xxx.vm and prepare it for writing. 
4. Use the CompilationEngine (along with VMWriter) to compile the parsed .jack class into .vm code.
5. Write the compiled .vm code to the .vm output file.

"""
import os
import sys
from jack_tokenizer import JackTokenizer
from syntax_analyzer import SyntaxAnalyzer
from compilation_engine import CompilationEngine


class JackCompiler:

    def __init__(self, path):
        """Gets all .jack files and for each one, compiles the appropriate VM code.

        Arguments: path -- the filepath to .jack file or directory (string)

        """
        # Finds all .jack files
        jack_files = self._get_jack_files(path)
        for jack_file in jack_files:
            self._compile(jack_file)
        

    def _get_jack_files(self, path):
        """Cehcks whether directory (containing .jack files?) or file and gets all .jack files.

        Arguments: path -- the filepath to .jack file or to directory (string)
        Returns: jack_files -- a list of .jack files (list)

        """
        if os.path.isdir(path):
            jack_files = [os.path.join(path, f) for f in os.listdir(path) if f.lower().endswith('.jack')]
            if len(jack_files) == 0:
                raise IOError("No .jack files in directory: %s" %path)
        elif os.path.isfile(path):
            jack_files = [path]
        else:
            raise IOError("%s is not a file or directory." %path)

        return jack_files

    def _compile(self, jack_file):
        """Compiles jack file into VM code.

        Creates JackTokenizer to tokenize .jack file. Creates SyntaxAnalyzer to parse list of tokens returned from JackTokenizer.  Parsed structure returned by SyntaxAnalyzer passed to CompilationEngine for compilation of VM code. List of VM commands returned by compiler written to .vm output file.

        Arguments: jack_file -- the .jack file to parse (string)

        """
        (jack_filename, jack_extension) = os.path.splitext(jack_file)
        vm_file = jack_filename + ".vm"

        file = open(jack_file, 'r')
        input = ''.join(file.readlines())

        tokens = JackTokenizer.tokenize(input)
        parse_tree = SyntaxAnalyzer.parse(tokens)
        compiler = CompilationEngine()
        compiled_code = compiler.compile_vm_code(parse_tree)
            
        output = open(vm_file, 'w')
        output.write(compiled_code)
        
        file.close()
        output.close()


# Main
if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Usage: %s [.jack file or directory ontaining .jack files]" %sys.argv[0])
    JackCompiler(sys.argv[1])

