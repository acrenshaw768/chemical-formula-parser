from antlr4 import *
from VisitorInterp import VisitorInterp
from build.ExprLexer import ExprLexer
from build.ExprParser import ExprParser

class ChemicalParser():
    def get_parser(stream):
        lexer = ExprLexer(stream)
        stream = CommonTokenStream(lexer)
        parser = ExprParser(stream)
        return parser
        
    def parse(stream):
        parser = ChemicalParser.get_parser(stream)
        tree = parser.program()
        if parser.getNumberOfSyntaxErrors() > 0:
            print("WARNING: syntax errors")
        vinterp = VisitorInterp()
        vinterp.visit(tree)
        reaction = vinterp.result
        return reaction
    
    def parse_molecule(stream):
        parser = ChemicalParser.get_parser(stream)
        tree = parser.summable_molecule()
        if parser.getNumberOfSyntaxErrors() > 0:
            print("WARNING: syntax errors")
        vinterp = VisitorInterp()
        vinterp.visit(tree)
        return vinterp.result
        
