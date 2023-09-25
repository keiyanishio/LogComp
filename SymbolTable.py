class SymbolTable:
    def __init__(self):
        self.table = {}

    def setter(self, key, value):
        self.table[key] = value
        
    def getter(self, key):
        return self.table[key]