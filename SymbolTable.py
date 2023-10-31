class SymbolTable:
    def __init__(self):
        self.table = {}
        self.sp = 0

    def setter(self, key, value):
        if value[1] != self.table[key][1]:
            raise SyntaxError("Tipo não combina") 
        self.table[key] = value
        
    def getter(self, key):
        return self.table[key]
    
    def create(self, key, value, tipo):
        if key in self.table.keys():
            raise SyntaxError("Essa variável já existe")
        else:
            self.sp += 4
            self.table[key] = (value, tipo, self.sp)