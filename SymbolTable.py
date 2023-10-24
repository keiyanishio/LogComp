class SymbolTable:
    def __init__(self):
        self.table = {}

    def setter(self, key, value):
        if value[0] != self.table[key][0]:
            raise SyntaxError("Tipo não combina: "+value[0]+"!="+self.table[key][0]) 
        self.table[key] = value
        
    def getter(self, key):
        return self.table[key]
    
    def create(self, key, value):
        if key in self.table.keys():
            raise SyntaxError("Essa variável já existe")
        else:
            self.table[key] = value