import sys
from antlr4 import *
from build.ExprParser import ExprParser
from build.ExprParserVisitor import ExprParserVisitor
import chemical

class VisitorInterp(ExprParserVisitor):
    def __init__(self):
        self.result = None
        
    def visitReaction(self, ctx:ExprParser.ReactionContext):
        self.result = chemical.Reaction(ctx)
        
    def visitSummable_molecule(self, ctx:ExprParser.Summable_moleculeContext):
        self.result = chemical.SummableMolecule(ctx)

