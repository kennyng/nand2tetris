#!/usr/bin/env python
"""THe JackGrammar Module.

Describes and represents the syntax of the Jack language as specified in Figure 10.5 'Complete grammar of the JAck language.' Encapsulates each grammar rule as a class object that maintains structure of code.
EXPORTED CLASSES: JackGrammar

"""
import syntax_elements as se


class JackGrammar:

    RULES = [
        
        # 'class' ClassName '{' ClassVarDec* SubroutineDec* '}'
        ("Class", ["sequence", "keywordclass", "ClassName", "symbol{", "ClassVarDecs", "SubroutineDecs", "symbol}"],
         lambda res: se.Class(res[2], res[4], res[5])),

        ("ClassVarDecs", ["list", "ClassVarDec"],
         lambda res: res[1:]),

        ("SubroutineDecs", ["list", "SubroutineDec"],
         lambda res: res[1:]),

        # ('static' | 'field') Type VarName (',' VarName)* ';'
        ("ClassVarDec", ["sequence", "DecScope", "Type", "VarName", "CommaPrecededVarNames", "symbol;"],
         lambda res: se.ClassVarDec(res[1], res[2], [res[3]] + res[4])),

        ("DecScope", ["type", "keywordstatic", "keywordfield"],
         lambda res: res[1]),

        ("CommaPrecededVarNames", ["list", "CommaPrecededVarName"],
         lambda res: res[1:]),

        ("CommaPrecededVarName", ["sequence", "symbol,", "VarName"],
         lambda res: res[2]),

        # 'int' | 'char' | 'boolean' | ClassName
        ("Type", ["type", "keywordint", "keywordchar", "keywordboolean", "ClassName"],
         lambda res: se.VarType(res[1])),
        
        # ('constructor' | 'fnction' | 'method') ('void' | Type) SubroutineName '(' ParameterList ')' SubroutineBody
        ("SubroutineDec", ["sequence", "SubroutineType", "SubroutineReturnType", "SubroutineName", "symbol(", "ParameterList", "symbol)", "SubroutineBody"],
         lambda res: se.SubroutineDec(res[1], res[2], res[3], res[5], res[7])),
      
        ("SubroutineType", ["type", "keywordconstructor", "keywordfunction", "keywordmethod"],
         lambda res: res[1]),

        ("SubroutineReturnType", ["type", "keywordvoid", "Type"],
         lambda res: res[1]),
      
        # ((Type VarName) (',' Type VarName)*)?
        ("ParameterList", ["optional", "NonEmptyParameterList"],
         lambda res: res[1] if len(res) > 1 else []),
      
        ("NonEmptyParameterList", ["sequence", "Type", "VarName", "CommaPrecededTypedVarNames"],
         lambda res: [(res[1], res[2])] + res[3]),

        ("CommaPrecededTypedVarNames", ["list", "CommaPrecededTypedVarName"],
         lambda res: res[1:]),

        ("CommaPrecededTypedVarName", ["sequence", "symbol,", "Type", "VarName"],
         lambda res: (res[2], res[3])),
      
        # '{' VarDec* Statements '}'
        ("SubroutineBody", ["sequence", "symbol{", "VarDecs", "Statements", "symbol}"],
         lambda res: se.SubroutineBody(res[2], res[3])),

        ("VarDecs", ["list", "VarDec"],
         lambda res: res[1:]),

        # 'var' Type VarName (',' VarName)* ';'
        ("VarDec", ["sequence", "keywordvar", "Type", "VarName", "CommaPrecededVarNames", "symbol;"], 
         lambda res: se.VarDec(res[2], [res[3]] + res[4])),

        ("ClassName", ["sequence", "Identifier"], 
         lambda res: res[1]),
        
        ("SubroutineName", ["sequence", "Identifier"], 
         lambda res: res[1]),
        
        ("VarName", ["sequence", "Identifier"], 
         lambda res: res[1]),
      
        # statement*
        ("Statements", ["list", "Statement"], 
         lambda res: se.Statements(res[1:])),
      
        # LetStatement | IfStatement | WhileStatement | DoStatement | ReturnStatement
        ("Statement", ["type", "LetStatement", "IfStatement", "DoStatement", "WhileStatement", "ReturnStatement"], 
         lambda res: se.Statement(res[1])),

        ("LetStatement", ["type", "RegularLetStatement", "ArrayEntryLetStatement"],
         lambda res: se.LetStatement(res[1])),

        # 'let' VarName '=' Expression ';'
        ("RegularLetStatement", ["sequence", "keywordlet", "VarName", "symbol=", "Expression", "symbol;"], 
         lambda res: se.RegularLetStatement(res[2], res[4])),

        # 'let' VarName ('[' Expression ']')? '=' Expression ';'
        ("ArrayEntryLetStatement", ["sequence", "keywordlet", "ArrayVarName", "symbol=", "Expression", "symbol;"],
         lambda res: se.ArrayEntryLetStatement(res[2][0], res[2][1], res[4])),

        ("IfStatement", ["type", "IfElseStatement", "RegularIfStatement"],
         lambda res: se.IfStatement(res[1])),

        # 'if' '(' Expression ')' '{' Statements '}'
        ("RegularIfStatement", ["sequence", "keywordif", "symbol(", "Expression", "symbol)", "symbol{", "Statements", "symbol}"], 
         lambda res: se.RegularIfStatement(res[3], res[6])),
        
        # RegularIfStatement ('else' '{' statement ']')?)
        ("IfElseStatement", ["sequence", "RegularIfStatement", "keywordelse", "symbol{", "Statements", "symbol}"],
         lambda res: se.IfElseStatement(res[1].expression, res[1].statements, res[4])),

        # 'while' '(' Expression ')' '{' Statements '}'
        ("WhileStatement", ["sequence", "keywordwhile", "symbol(", "Expression", "symbol)", "symbol{", "Statements", "symbol}"],
         lambda res: se.WhileStatement(res[3], res[6])),

        # 'do' SubroutineCall ';'
        ("DoStatement", ["sequence", "keyworddo", "SubroutineCall", "symbol;"],
         lambda res: se.DoStatement(res[2])),
      
        ("ReturnStatement", ["type", "ReturnExpressionStatement", "ReturnToEndStatement"], 
         lambda res: se.ReturnStatement(res[1])),
      
        # 'return' Expression ';'
        ("ReturnExpressionStatement", ["sequence", "keywordreturn", "Expression", "symbol;"], 
         lambda res: se.ReturnExpressionStatement(res[2])),

        # 'return' ';'
        ("ReturnToEndStatement", ["sequence", "keywordreturn", "symbol;"], 
         lambda res: se.ReturnToEndStatement()),

        # Term (OpTerm)*
        ("Expression", ["sequence", "Term", "OpTerms"], 
         lambda res: se.Expression(res[1], res[2])),
        
        ("OpTerms", ["list", "OpTerm"], 
         lambda res: res[1:]),
        
        ("OpTerm", ["sequence", "Op", "Term"], 
         lambda res: (res[1], res[2])),
        
        ("Term", ["type", "IntegerConstant", "KeywordConstant", "StringConstant", "SubroutineCall", "ArrayVarName", "VarName", "ParenExpression", "UnaryOpTerm"],
         lambda res: se.Term(res[1])),
      
        ("ArrayVarName", ["sequence", "VarName", "symbol[", "Expression", "symbol]"], 
         lambda res: (res[1], res[3])),

        ("ParenExpression", ["sequence", "symbol(", "Expression", "symbol)"], 
         lambda res: res[2]),

        ("UnaryOpTerm", ["sequence", "UnaryOp", "Term"], 
         lambda res: se.UnaryOpTerm(res[1], res[2])),
      
        ("SubroutineCall", ["type", "FunctionCall", "MethodCall", "StaticMethodCall"], 
         lambda res: se.SubroutineCall(res[1])),

        ("FunctionCall", ["sequence", "SubroutineName", "symbol(", "ExpressionList", "symbol)"], 
         lambda res: se.FunctionCall(res[1], res[3])),

        ("MethodCall", ["sequence", "VarName", "symbol.", "SubroutineName", "symbol(", "ExpressionList", "symbol)"],
         lambda res: se.MethodCall(res[1], res[3], res[5])),

        ("StaticMethodCall", ["sequence", "ClassName", "symbol.", "SubroutineName", "symbol(", "ExpressionList", "symbol)"], 
         lambda res: se.StaticMethodCall(res[1], res[3], res[5])),

        ("ExpressionList", ["optional", "NonEmptyExpressionList"],
         lambda res: res[1] if len(res) > 1 else []),
      
        ("NonEmptyExpressionList", ["sequence", "Expression", "CommaPrecededExpressions"],
         lambda res: [res[1]] + res[2]),
        
        ("CommaPrecededExpressions", ["list", "CommaPrecededExpression"],
         lambda res: res[1:]),
        
        ("CommaPrecededExpression", ["sequence", "symbol,", "Expression"],
         lambda res: res[2]),
      
        ("Op", ["type", "symbol+", "symbol-", "symbol*", "symbol/", "symbol&", "symbol|", "symbol<", "symbol>", "symbol="],
         lambda res: se.Op(res[1])),
        
        ("UnaryOp", ["type", "symbol-", "symbol~"], 
         lambda res: se.UnaryOp(res[1])),
      
        ("KeywordConstant", ["type", "keywordtrue", "keywordfalse", "keywordnull", "keywordthis"], 
         lambda res: se.KeywordConstant(res[1]))
        
        ]


