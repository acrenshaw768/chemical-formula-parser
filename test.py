import unittest
from antlr4 import *
from parser import ChemicalParser

class Test(unittest.TestCase):

    def test1(self):
        testString = "C7H16(l)+O2(g)->CO2(g)+H2O(g)"
        reaction = ChemicalParser.parse(InputStream(testString))
        self.assertFalse(reaction.isBalanced())
        self.assertNotEqual(reaction.lhs.weigh(), reaction.rhs.weigh())
        
    def test2(self):
        testString = "C7H16(l)+11O2(g)->7CO2(g)+8H2O(g)"
        reaction = ChemicalParser.parse(InputStream(testString))
        self.assertTrue(reaction.isBalanced())
        self.assertEqual(reaction.lhs.weigh(), reaction.rhs.weigh())
        
    def test3(self):
        testString = "C8H18(l)+O2(g)->CO2(g)+H2O(g)"
        reaction = ChemicalParser.parse(InputStream(testString))
        self.assertFalse(reaction.isBalanced())
        self.assertNotEqual(reaction.lhs.weigh(), reaction.rhs.weigh())
        
    def test4(self):
        testString = "2C8H18(l)+25O2(g)->16CO2(g)+18H2O(g)"
        reaction = ChemicalParser.parse(InputStream(testString))
        self.assertTrue(reaction.isBalanced())
        self.assertEqual(reaction.lhs.weigh(), reaction.rhs.weigh())
        
    def test5(self):
        testString = "C+25O2->48O + CO2"
        reaction = ChemicalParser.parse(InputStream(testString))
        self.assertTrue(reaction.isBalanced())
        self.assertEqual(reaction.lhs.weigh(), reaction.rhs.weigh())
        
    def test6(self):
        testString = "[C](O2)6+25O2->12O + C + 10O5"
        reaction = ChemicalParser.parse(InputStream(testString))
        self.assertTrue(reaction.isBalanced())
        self.assertEqual(reaction.lhs.weigh(), reaction.rhs.weigh())
        
    def test7(self):
        testString = "Ca5(PO4)3(OH)(s)+H3PO4(aq)+H2O(l)->Ca(H2PO4)2.H2O(s)"
        reaction = ChemicalParser.parse(InputStream(testString))
        self.assertFalse(reaction.isBalanced())
        self.assertNotEqual(reaction.lhs.weigh(), reaction.rhs.weigh())
        
    def test8(self):
        testString = "Ca5(PO4)3(OH)(s)+7H3PO4(aq)+4H2O(l)->5Ca(H2PO4)2.H2O(s)"
        reaction = ChemicalParser.parse(InputStream(testString))
        self.assertTrue(reaction.isBalanced())
        self.assertEqual(reaction.lhs.weigh(), reaction.rhs.weigh())
        
    def test9(self):
        testString = "C6H12O6(s)->2C2H5OH(l)+2CO2(g)"
        reaction = ChemicalParser.parse(InputStream(testString))
        self.assertTrue(reaction.isBalanced())
        self.assertEqual(reaction.lhs.weigh(), reaction.rhs.weigh())
        
    def test10(self):
        testString = "C14H18N2O5"
        molecule = ChemicalParser.parse_molecule(InputStream(testString))
        self.assertEqual(round(molecule.ratios()["C"], 2), 0.57)
        
        
if __name__ == '__main__':
    unittest.main()
