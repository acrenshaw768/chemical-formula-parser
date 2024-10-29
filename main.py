import sys, os
from antlr4 import *
from parser import ChemicalParser

def main(argv):
    reaction = ChemicalParser.parse(FileStream(argv[1]))
    print(reaction.lhs.weigh())
    
if __name__ == '__main__':
    main(sys.argv)
