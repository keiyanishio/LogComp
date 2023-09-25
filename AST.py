
class Node:
    def __init__(self, value, children):
        self.value = value 
        self.children = children
        

    def evaluate(self, ST):
        pass
    
class BinOp(Node):
    def evaluate(self, ST):
        if self.value == "+":
            return self.children[0].evaluate(ST) + self.children[1].evaluate(ST)
        
        elif self.value == "-":
            return self.children[0].evaluate(ST) - self.children[1].evaluate(ST)
        
        elif self.value == "*":
            return self.children[0].evaluate(ST) * self.children[1].evaluate(ST)
        
        elif self.value == "/":
            return self.children[0].evaluate(ST) // self.children[1].evaluate(ST)

class UnOp(Node):
    def evaluate(self, ST):
        if self.value == "+":
            return self.children[0].evaluate(ST)
        else:
            return -self.children[0].evaluate(ST)
        
class IntVal(Node):
    def evaluate(self, ST):
        return self.value

class NoOp(Node):
    def evaluate(self, ST):
        pass
    
#####################################
class Assigment(Node):
    def evaluate(self, ST):
        return ST.setter(self.children[0].value, self.children[1].evaluate(ST))
    
    
class Identifier(Node):
    def evaluate(self, ST):
        return ST.getter(self.value)
            

class Block(Node):
    def evaluate(self, ST):
        for child in self.children:
            child.evaluate(ST)
            
class Print(Node):
    def evaluate(self, ST):
        print(self.children[0].evaluate(ST))
        #print("Debug")
        return 0
