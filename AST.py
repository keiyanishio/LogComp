
class Node:
    def __init__(self, value, children):
        self.value = value 
        self.children = children
        

    def evaluate(self, ST):
        pass
    
class BinOp(Node):
    def evaluate(self, ST):
        
        if self.children[0].evaluate(ST)[1] == self.children[1].evaluate(ST)[1]:
        
            if self.value == "+":
                return (self.children[0].evaluate(ST)[0] + self.children[1].evaluate(ST)[0], "int")
            
            elif self.value == "-":
                return (self.children[0].evaluate(ST)[0] - self.children[1].evaluate(ST)[0], "int")
            
            elif self.value == "*":
                return (self.children[0].evaluate(ST)[0] * self.children[1].evaluate(ST)[0], "int")
            
            elif self.value == "/":
                return (self.children[0].evaluate(ST)[0] / self.children[1].evaluate(ST)[0], "int")
            
            elif self.value == "&&":
                return (int(self.children[0].evaluate(ST)[0] and self.children[1].evaluate(ST)[0]), "int")
            
            elif self.value == "||":
                return (int(self.children[0].evaluate(ST)[0] or self.children[1].evaluate(ST)[0]), "int")
            
            elif self.value == "<":
                return (int(self.children[0].evaluate(ST)[0] < self.children[1].evaluate(ST)[0]), "int")
            
            elif self.value == ">":
                return (int(self.children[0].evaluate(ST)[0] > self.children[1].evaluate(ST)[0]), "int")
            
            elif self.value == "==":
                return (int(self.children[0].evaluate(ST)[0] == self.children[1].evaluate(ST)[0]), "int")
            
            elif self.value == ".":
                return (self.children[0].evaluate(ST)[0] + self.children[1].evaluate(ST)[0], "string")
        else:
            raise SyntaxError("Tipos errados")
            

class UnOp(Node):
    def evaluate(self, ST):
        if self.value == "+":
            return (self.children[0].evaluate(ST)[0], "int")
        elif self.value == "!":
            return (not self.children[0].evaluate(ST)[0], "int")
        else:
            return (-self.children[0].evaluate(ST)[0], "int")
        
class IntVal(Node):
    def evaluate(self, ST):
        return (int(self.value), "int")

class NoOp(Node):
    def evaluate(self, ST):
        pass
    
##########################################################################
class Assigment(Node):
    def evaluate(self, ST):
        ST.setter(self.children[0].value, self.children[1].evaluate(ST))
    
    
class Identifier(Node):
    def evaluate(self, ST):
        valor =  ST.getter(self.value)
        if valor.isalpha():
            return (valor, "string")
        
        elif valor.isdigit():
            return (valor, "int")
            
            

class Block(Node):
    def evaluate(self, ST):
        for child in self.children:
            child.evaluate(ST)
            
class Print(Node):
    def evaluate(self, ST):
        print(self.children[0].evaluate(ST))
        return 0
    
########################################################################
class Scan(Node):
    def evaluate(self, ST):
        return (int(input()), "int")


class ForLoop(Node):
    def evaluate(self, ST):
        self.children[0].evaluate(ST)
        while self.children[1].evaluate(ST):
            self.children[3].evaluate(ST)
            self.children[2].evaluate(ST)
            
class IfCond(Node):
    def evaluate(self, ST):
        if self.children[0].evaluate(ST):
            self.children[1].evaluate(ST)
        elif (len(self.children)>2):
            self.children[2].evaluate(ST)
            
########################################################################
class VarDec(Node):
    def evaluate(self, ST):
        if len(self.children) <= 1:
            if self.value == "int":
                ST.create(self.children[0].value, (self.value, 0))
            elif self.value == "string":
                ST.create(self.children[0].value, (self.value, ""))
            
        else:
            ST.create(self.children[0].value, (self.value, self.children[1].evaluate()[1]))
            
            
class StrVal(Node):
    def evaluate(self, ST):
        return (self.value, "string")
