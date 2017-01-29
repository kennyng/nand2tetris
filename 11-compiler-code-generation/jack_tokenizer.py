#!/usr/bin/env python
"""The JackTokenizer Module.

Handles the tokenizing (breaking program elements into tokens) of a single .jack file and
encapuslates access to the input code.
EXPORTED CLASSES: JackTokenizer

"""
import os
import re
import syntax_elements


class JackTokenizer:
    """Removes all comments and whitespace from input stream and breaks it into Jack-language tokens, as specified by the Jack grammar."""
    
    _RE_KEYWORD = re.compile(
        r"(?:"
        r"class|constructor|function|method|"
        r"field|static|var|int|char|boolean|"
        r"void|true|false|null|this|let|do|"
        r"if|else|while|return"
        r")(?=[^a-zA-Z0-9_])")
        
    _RE_SYMBOL = re.compile("[%s]" % (re.escape(r"{}()[].,;+-*/&|<>=~")))
        
    _RE_IDENTIFIER = re.compile(r"[a-zA-Z_][a-zA-Z_0-9]*")
    
    _RE_INT_CONST = re.compile(r"\d+")
    
    _RE_STRING_CONST = re.compile(r"\"[^\"\r\n]*\"")
    
    _RE_WHITESPACE = re.compile(r"\s")
    
    _RE_INLINE_COMMENT = re.compile(r"//[^\n\r]*[^\n\r]")

    _RE_MULTILINE_COMMENT = re.compile(r"/\*.*?\*/", re.DOTALL)

    _RE_END_OF_LINE = re.compile(r"[^\n\r]*")

    _TOKEN_REGEX_TYPES = [
        (_RE_WHITESPACE, None),
        (_RE_INLINE_COMMENT, None),
        (_RE_MULTILINE_COMMENT, None),
        (_RE_KEYWORD, syntax_elements.Keyword),
        (_RE_SYMBOL, syntax_elements.Symbol),
        (_RE_INT_CONST, syntax_elements.IntegerConstant), 
        (_RE_STRING_CONST, syntax_elements.StringConstant),	   
        (_RE_IDENTIFIER, syntax_elements.Identifier)
    ]


    @staticmethod
    def tokenize(file):
        """Breaks the syntax elements within a Jack program file into tokens (terminal elements).

        Argument: file -- the Jack input file prepared for reading
        Returns: list of tokens
        
        """
        tokens = []
        pos = 0
        line_num = 0
        size = len(file)

        while pos < size:
            match = None
            current_token = None

            for regex, type in JackTokenizer._TOKEN_REGEX_TYPES:
                match = regex.match(file, pos)
                if match:
                    if type: current_token = type(match.group(0).replace("\"", ""))
                    break
            
            if match:
                pos += len(match.group(0))
                line_num += match.group(0).count(os.linesep)
                if current_token: tokens.append(current_token)
            else:
                raise TokenizerError("Tokenizer Error on line %d: %s" %(line + 1, JackTokenizer._RE_END_OF_LINE.match(file, pos).group(0)))
        
        return tokens


class TokenizerError(Exception):
    """For tokenizer error exceptions; null operation -- nothing happens.""" 
    pass

