#!/usr/bin/env python
"""The JackAnalyzer Module.

The analyzer program operates on a given source, where source is either a filename of the form Xxx.jack 
or a directory name containing on or more .jack files. For each source Xxx.jack, the analyzer goes through
the following logic:
1. Create a JackTokenizer from the Xxx.jack input file.
2. Create an output file called Xxx.xml and prepare it for writing.
3. Use the CompilationEngine to compile the input JackTokenizer into the output file.

"""
import os
import sys
from jack_tokenizer import JackTokenizer
from compilation_engine import CompilationEngine


class JackAnalyzer:
    def __init__(self, path):
        """Gets all .jack files and for each one, outputs the appropriate xml file.

        Arguments: path -- the filepath to .jack file or directory (string)

        """
        # Finds all .jack files
        jack_files = self._get_jack_files(path)
        for jack_file in jack_files:
            self._output_xml(jack_file)

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

    def _output_xml(self, jack_file):
        """Creates a JackTokenizer and opens xml file, passes to CompilationEngine for parsing.

        Arguments: jack_file -- the .jack file to parse (string)

        """
        (jack_filename, jack_extension) = os.path.splitext(jack_file)
        xml_file = jack_filename + "FULL.xml"

        tokenizer = JackTokenizer(jack_file)
        xml_output = open(xml_file, 'w')
        compiler = CompilationEngine(tokenizer, xml_output)
        tokenizer.close()
        xml_output.close()


# Main
if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Usage: %s [.jack fiel or directory ontaining .jack files]" %sys.argv[0])
    JackAnalyzer(sys.argv[1])

