from counter import Counter
import json

with open("properties/properties.json","r") as f:
    symbol_lookup = {}
    for elem in json.load(f):
        symbol_lookup[elem["Symbol"]] = elem

class Countable():
    def __init__(self):
        self.counter = None
        
    def count(self):
        self.counter = Counter()
        return self.counter
    
class Weightable(Countable):
    def __init__(self):
        self.counter = None
        self.weight = None
        
    def count(self):
        if not self.counter:
            self.counter = Counter()
        return self.counter
        
    def weigh(self) -> int:
        if not self.weight:
            counter = self.count().count
            self.weight = {}
            for key in counter.keys():
                self.weight[key] = symbol_lookup[key]["Weight"] * counter[key]
        return sum(self.weight.values())
        
    def ratios(self):
        ratios = {}
        total = self.weigh()
        for key in self.weight.keys():
            ratios[key] = self.weight[key] / total
        return ratios
        

class Reaction():
    def __init__(self, ctx):
        self.lhs = MoleculeSum(ctx.lhs)
        self.rhs = MoleculeSum(ctx.rhs)
        
    def isBalanced(self) -> bool:
        return self.lhs.count().equals(self.rhs.count())
        
    def __str__(self):
        return str(self.lhs) + " -> " + str(self.rhs)
        
class MoleculeSum(Weightable):
    def __init__(self, ctx):
        super().__init__()
        self.summable_molecules = [
            SummableMolecule(x) for x in ctx.summable_molecule()
        ]
    
    def count(self) -> Counter:
        if not self.counter:
            self.counter = Counter()
            for i in range(len(self.summable_molecules)):
                self.counter.add(self.summable_molecules[i].count())
        return self.counter
        
    def __str__(self):
        return " + ".join([
            str(self.summable_molecules[i]) 
            for i in range(len(self.summable_molecules))
        ])
        
class Mult():
    def __init__(self, ctx):
        if ctx:
            self.mult = int(ctx.INT().getText())
        else :
            self.mult = 1
    
    def __str__(self):
        return str(self.mult)
        
class SummableMolecule(Weightable):
    def __init__(self, ctx):
        super().__init__()
        if ctx.molecule():
            self.molecule = Molecule(ctx.molecule())
        else:
            self.molecule = StatefulMolecule(ctx.stateful_molecule())
        self.mult = Mult(ctx.mult())
            
    def count(self) -> Counter:
        if not self.counter:
            self.counter = self.molecule.count().multiply(self.mult)
        return self.counter
    
    def __str__(self):
        return str(self.mult) + "*(" +str(self.molecule) + ")"
            
class StatefulMolecule(Weightable):
    def __init__(self, ctx):
        super().__init__()
        self.state = ctx.state_().getText()
        self.molecule = Molecule(ctx.molecule())
        
    def count(self) -> Counter:
        if not self.counter:
            self.counter = self.molecule.count()
        return self.counter
        
    def __str__(self):
        return str(self.molecule) + str(self.state)
        
class Molecule(Weightable):
    def __init__(self, ctx):
        super().__init__()
        if ctx.stoichiometric_coefficient():
            self.submolecules = [
                Molecule(x) for x in ctx.molecule()
            ]
            self.mult = [
                Mult(None), 
                Mult(ctx.stoichiometric_coefficient().mult())
            ]
        else:
            self.submolecules = [
                WrappableMolecule(x) for x in ctx.wrappable_molecule()
            ]
            self.mult = [
                Mult(None) for x in ctx.wrappable_molecule()
            ]
            
    def count(self) -> Counter:
        if not self.counter:
            self.counter = Counter()
            for i in range(len(self.mult)):
                self.counter.add(self.submolecules[i].count().multiply(self.mult[i]))
        return self.counter
    
    def __str__(self):
        s = "<>".join([
            str(self.mult[i]) + "*" + "(" + str(self.submolecules[i]) + ")" 
            for i in range(len(self.mult))
        ])
        return s
            
class WrappableMolecule(Weightable):
    def __init__(self, ctx):
        super().__init__()
        if ctx.homonuclear():
            self.homonuclears = [Homonuclear(x) for x in ctx.homonuclear()]
        else:
            self.homonuclears = []
        if ctx.wrappable_molecule():
            self.submolecule = WrappableMolecule(ctx.wrappable_molecule())
            self.mult = Mult(ctx.mult())
        else:
            self.submolecule = None
            self.mult = None
            
    def count(self) -> Counter:
        if not self.counter:
            self.counter = Counter()
            for h in self.homonuclears:
                self.counter.add(h.count())
            if self.submolecule:
                self.counter.add(self.submolecule.count().multiply(self.mult))
        return self.counter
    
    def __str__(self):
        s = ""
        if self.submolecule:
            s = str(self.mult) + "*" + "(" + str(self.submolecule) + ")"
        if self.homonuclears:
            if self.submolecule:
                s = s + "<>" 
            s = s + "<>".join([
                str(homonuclear) for homonuclear in self.homonuclears
            ])
        return s
        
class Homonuclear(Weightable):
    def __init__(self, ctx):
        super().__init__()
        self.elem = Element(ctx.elem())
        self.isotope = Isotope(ctx.isotope())
        self.mult = Mult(ctx.mult())
        
    def count(self) -> Counter:
        if not self.counter:
            self.counter = self.elem.count().add(self.isotope.count()).multiply(self.mult)
        return self.counter
        
    def __str__(self):
        if self.elem:
            return str(self.elem) + str(self.mult)
        else:
            return str(self.isotope) + str(self.mult) 
        
class Element(Weightable):
    def __init__(self, ctx):
        super().__init__()
        if ctx:
            self.id = ctx.ID()
            
    def count(self) -> Counter:
        if not self.counter:
            if self.id:
                self.counter = Counter(str(self.id), 1)
            else:
                self.counter = Counter()
        return self.counter
            
    def __str__(self):
        return str(self.id)
        
class Isotope(Weightable):
    def __init__(self, ctx):
        super().__init__()
        if ctx:
            self.id = ctx.elem().ID()
            self.num = ctx.INT()
        else:
            self.id = None
            self.num = None
            
    def count(self) -> Counter:
        ## TODO does num matter here??
        if not self.counter:
            if self.id:
                self.counter = Counter(str(self.id) + str(self.num), 1)
            else:
                self.counter = Counter()
        return self.counter
        
    def __str__(self):
        return str(self.id) + "_" + str(self.num)

