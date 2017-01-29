#!/usr/bin/env python
"""The SyntaxAnalyzer Module.

Reads a list of tokens from a Jack program and determines its syntactic structure with respect to the Jack grammar.
EXPORTED CLASS: SyntaxAnalyzer

"""
import os
import syntax_elements as se
from jack_grammar import JackGrammar


class SyntaxAnalyzer:
    
    def __init__(self, tokens):
        """Generates and calls the appropriate parser for each grammar rule specified in the Jack grammar."""
        self._size = len(tokens)
        self._tokens = tokens
  
        for rule in JackGrammar.RULES:
            function = getattr(self, "%s_parser" % (rule[1][0],))
            function(rule[0], rule[1][1:], rule[2])

    @staticmethod
    def parse(tokens):
        """Takes a list fo token and parses recursively from the top-down, starting with parse_Class."""
        syntax_analyzer = SyntaxAnalyzer(tokens)
        parser = getattr(syntax_analyzer, "parse_Class")
        parse_tree, index = parser(0)

        if index < len(tokens):
            raise ParserError("NOT ALL TOKENS PARSED.")
        else:
            return parse_tree
 
    def get_parser(self, element, index):
        """Gets the parser as specified in JackGrammar.RULES."""
        if element.startswith("keyword"):
            return self.parse_Keyword(element[7:], index)
        elif element.startswith("symbol"):
            return self.parse_Symbol(element[6:], index)
        else:
            return getattr(self, "parse_" + element)(index)

    def sequence_parser(self, name, sequence, syntax_structure):
        """Parses a sequence of tokens (for program structure, statements, expressions) """
        def parser(self, index):
            try:
                result = []
                result.append(name)
                i = index
                for element in sequence:
                    res, i = self.get_parser(element, i)
                    result.append(res)
                return syntax_structure(result), i
            except ParserError as error:
                raise ParserError("CANNOT PARSE " + name + os.linesep)
        
        setattr(SyntaxAnalyzer, "parse_" + name, parser)

    def type_parser(self, name, options, syntax_structure):
        """Parses the grammar rule in which a choice must be specified (var types, declarations, and different types of statements."""
        def parser(self, index):
            i = index
            for element in options:
                try:
                    res, i = self.get_parser(element, i)
                    return syntax_structure([name, res]), i
                except ParserError as error:
                    pass
            raise ParserError("CANNOT PARSE " + name)
   
        setattr(SyntaxAnalyzer, "parse_" + name, parser)

    def list_parser(self, name, item, syntax_structure):
        """Parses a list of tokens (parameters, expressions, etc.)."""
        def parser(self, index):
            result = []
            result.append(name)
            i = index
            try:
                while True:
                    res, i = self.get_parser(item[0], i)
                    result.append(res)
            except ParserError as error:
                return syntax_structure(result), i

        setattr(SyntaxAnalyzer, "parse_" + name, parser)

    def optional_parser(self, name, item, syntax_structure):
        """Parses optional syntax elements within the grammar (parameters, expressions, etc.)."""
        def parser(self, index):
            result = []
            result.append(name)
            i = index
            try:
                res, i = self.get_parser(item[0], i)
                result.append(res)
                return syntax_structure(result), i
            except ParserError as error:
                return syntax_structure(result), i

        setattr(SyntaxAnalyzer, "parse_" + name, parser)

    def parse_Keyword(self, keyword, index):
        """Returns keyword as class object."""
        token = self._get_next_token(index)
        if token and token.__class__.__name__ == "Keyword" and token.keyword == keyword:
            return se.Keyword(keyword), index + 1
        else:
            raise ParserError("CANNOT PARSE KEYWORD: %s" % (keyword,))

    def parse_Symbol(self, symbol, index):
        """Returns symbol as class object."""
        token = self._get_next_token(index)
        if token and token.__class__.__name__ == "Symbol" and token.symbol == symbol:
            return se.Symbol(symbol), index + 1
        else:
            raise ParserError("CANNOT PARSE SYMBOL: %s" % (symbol,))

    def parse_IntegerConstant(self, index):
        """Returns interger constant as class object."""
        token = self._get_next_token(index)
        if token and token.__class__.__name__ == "IntegerConstant":
            return se.IntegerConstant(token.integer_constant), index + 1
        else:
            raise ParserError("CANNOT PARSE INTEGER CONSTANT")

    def parse_StringConstant(self, index):
        """Returns string constant as class object."""
        token = self._get_next_token(index)
        if token and token.__class__.__name__ == "StringConstant":
            return se.StringConstant(token.string_constant), index + 1
        else:
            raise ParserError("CANNOT PARSE STRING CONSTANT")

    def parse_Identifier(self, index):
        """Returns an identifier as class object."""
        token = self._get_next_token(index)
        if token and token.__class__.__name__ == "Identifier":
            return se.Identifier(token.identifier), index + 1
        else:
            raise ParserError("CANNOT PARSE IDENTIFIER")

    def _get_next_token(self, index):
        """Gets the next token from the list of tokens if there are more tokens."""
        return self._tokens[index] if index < self._size else None


class ParserError(Exception):
    """For tokenizer error exceptions; null operation -- nothing happens.""" 
    pass

