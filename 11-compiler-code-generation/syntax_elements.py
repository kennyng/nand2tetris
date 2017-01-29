#!/usr/bin/env python
"""The SyntacticElements Module.

Represents the Jack language syntax elements as shown in Figure 10.5 (Page 208-209).
EXPORTED CLASSES: 
[Lexical Elements]
Keyword, Symbol, IntegerConstant, StringConstant, Identifier
[Program Structure]
Class, ClassVarDec, VarType, SubroutineDec, SubroutineBody, VarDec, ClassName, SubroutineName, VarName
[Statements]
Statements, Statement, LetStatementBasic, LetStatementFull, ArrayEntryLetStatement, IfStatementBasic, IfStatementFull, IfElseStatement, WhileStatement, DoStatement, ReturnStatement, ReturnExpressionStatement, ReturnToEndStatement
[Expressions]
Expression, Term, UnaryOpTerm, SubroutineCall, FunctionCall, MethodCall, StaticMethodCall, Op, UnaryOp, KeywordConstant 

"""

# Lexical Elements
class Keyword:
    def __init__(self, keyword):
        self.keyword = keyword

class Symbol:
    def __init__(self, symbol):
        self.symbol = symbol

class IntegerConstant:
    def __init__(self, integer_constant):
        self.integer_constant = integer_constant

class StringConstant:
    def __init__(self, string_constant):
        self.string_constant = string_constant

class Identifier:
    def __init__(self, identifier):
        self.identifier = identifier


# Program Structure
class Class:
    def __init__(self, class_name, class_var_decs, subroutine_decs):
        self.class_name =  class_name
        self.class_var_decs = class_var_decs
        self.subroutine_decs = subroutine_decs

class ClassVarDec:
    def __init__(self, scope, var_type, var_names):
        self.scope = scope
        self.var_type = var_type
        self.var_names = var_names

class VarType:
    def __init__(self, var_type):
        self.var_type = var_type

class SubroutineDec:
    def __init__(self, subroutine_type, return_type, name, parameter_list, body):
        self.subroutine_type = subroutine_type
        self.return_type = return_type
        self.name = name
        self.parameter_list = parameter_list
        self.body = body

class SubroutineBody:
    def __init__(self, var_decs, statements):
        self.var_decs = var_decs
        self.statements = statements

class VarDec:
    def __init__(self, var_type, var_names):
      self.var_type = var_type
      self.var_names = var_names

class ClassName:
    def __init__(self, identifier):
        self.identifier = identifier

class SubroutineName:
    def __init__(self, identifier):
        self.identifier = identifier

class VarName:
    def __init__(self, identifier):
        self.identifier = identifier


#Statements
class Statements:
    def __init__(self, statements):
        self.statements = statements

class Statement:
    def __init__(self, statement):
        self.statement = statement

class LetStatement:
    def __init__(self, let_statement):
        self.let_statement = let_statement

class RegularLetStatement:
    def __init__(self, var_name, expression):
        self.var_name = var_name
        self.expression = expression

class ArrayEntryLetStatement:
    def __init__(self, var_name, expression, exp_index):
        self.var_name = var_name
        self.expression = expression
        self.exp_index = exp_index

class IfStatement:
    def __init__(self, if_statement):
        self.if_statement = if_statement

class RegularIfStatement:
    def __init__(self, expression, statements):
        self.expression = expression
        self.statements = statements

class IfElseStatement:
    def __init__(self, expression, if_statements, else_statements):
        self.expression = expression
        self.if_statements = if_statements
        self.else_statements = else_statements

class WhileStatement:
    def __init__(self, expression, statements):
        self.expression = expression
        self.statements = statements

class DoStatement:
    def __init__(self, subroutine_call):
        self.subroutine_call = subroutine_call

class ReturnStatement:
    def __init__(self, return_statement):
        self.return_statement = return_statement

class ReturnExpressionStatement:
    def __init__(self, expression):
        self.expression = expression

class ReturnToEndStatement:
    def __init__(self):
        pass


# Expressions
class Expression:
    def __init__(self, first_term, op_term_list):
        self.first_term = first_term
        self.op_term_list = op_term_list

class Term:
    def __init__(self, term):
        self.term = term

class UnaryOpTerm:
    def __init__(self, op, term):
        self.op = op
        self.term = term

class SubroutineCall:
    def __init__(self, subroutine_call):
        self.subroutine_call = subroutine_call

class FunctionCall:
    def __init__(self, function_name, expression_list):
        self.function_name = function_name
        self.expression_list = expression_list

class MethodCall:
    def __init__(self, var_name, method_name, expression_list):
        self.var_name = var_name
        self.method_name = method_name
        self.expression_list = expression_list

class StaticMethodCall:
    def __init__(self, class_name, method_name, expression_list):
        self.class_name = class_name
        self.method_name = method_name
        self.expression_list = expression_list

class Op:
    def __init__(self, op):
        self.op = op

class UnaryOp:
    def __init__(self, op):
        self.op = op

class KeywordConstant:
    def __init__(self, constant):
        self.constant = constant


