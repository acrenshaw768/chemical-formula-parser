from typing import Self

class Counter():
    def __init__(self, key=None, value=None):
        self.count = {}
        if key and value:
            self.count[key] = value
        
    def add(self, add) -> Self:
        for k in add.count.keys():
            if k in self.count.keys():
                self.count[k] = self.count[k] + add.count[k]
            else:
                self.count[k] = add.count[k]
        return self
    
    def multiply(self, mult) -> Self:
        for k in self.count.keys():
            self.count[k] = self.count[k] * int(mult.mult)
        return self
    
    def equals(self, count) -> bool:
        return self.count == count.count
    
    def __str__(self):
        return str(self.count)
        
    def __repr__(self):
        return repr(self.count)
