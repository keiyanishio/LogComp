
class Writer:
    text = ''
    @staticmethod
    def write_start():
        with open("teste1.asm", "a") as f:
            with open("start.txt", "r") as start:
                f.write(start.read()) 
    
    @staticmethod
    def write_asm(code):
        Writer.text+=code
            
            
    @staticmethod
    def write_end():
        with open("teste1.asm", 'a') as file:
            with open("end.txt", "r") as end:
                file.write(Writer.text+end.read())
    

class Node:
    
    i = 0
    
    def __init__(self, value, children):
        self.value = value 
        self.children = children
        self.id = self.newId()

    def evaluate(self, ST):
        pass
    
    @staticmethod
    def newId():
        Node.i += 1
        return Node.i
    
class BinOp(Node):
    def evaluate(self, ST):
        self.children[1].evaluate(ST)
        Writer.write_asm("PUSH EAX")
        self.children[0].evaluate(ST) 
        Writer.write_asm("POP EBX")
        
        # print(left, right)
        
        
        if self.value == "+":
            Writer.write_asm("ADD EAX, EBX")
                
        elif self.value == "-":
            Writer.write_asm("SUB EAX, EBX")
        
        elif self.value == "*":
            Writer.write_asm("IMUL EBX")
        
        elif self.value == "/":
            Writer.write_asm("CDQ")
            Writer.write_asm("IDIV EBX") 
            
        elif self.value == "&&":
            Writer.write_asm("AND EAX, EBX")
        
        elif self.value == "||":
            Writer.write_asm("OR EAX, EBX")
        
        elif self.value == "<":
            Writer.write_asm("CMP EAX, EBX")
            Writer.write_asm("CALL binop_jl")
        
        elif self.value == ">":
            Writer.write_asm("CMP EAX, EBX")
            Writer.write_asm("CALL binop_jg")
        
        elif self.value == "==":
            Writer.write_asm("CMP EAX, EBX")
            Writer.write_asm("CALL binop_je")
        
        # elif self.value == ".":
        #     return (str(self.children[0].evaluate(ST)[0]) + str(self.children[1].evaluate(ST)[0]), "string")


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
        asm = "MOV EAX, "+self.value
        Writer.write_asm(asm)
        #return (int(self.value), "int")

class NoOp(Node):
    def evaluate(self, ST):
        pass
    
##########################################################################
class Assigment(Node):
    def evaluate(self, ST):
        self.children[1].evaluate(ST)
        identifier = ST.getter(self.value)
        sp = identifier[2]
        asm = "MOV [EBP-{}], EAX".format(sp)
        Writer.write_asm(asm)
    
    
class Identifier(Node):
    def evaluate(self, ST):
        identifier = ST.getter(self.value)
        sp = identifier[2]
        asm = "MOV EAX, [EBP-{}]".format(sp)
        Writer.write_asm(asm)
            
            

class Block(Node):
    def evaluate(self, ST):
        for child in self.children:
            child.evaluate(ST)
            
class Print(Node):
    def evaluate(self, ST):
        Writer.write_asm("PUSH EAX")
        Writer.write_asm("PUSH formatout")
        Writer.write_asm("CALL printf")
        Writer.write_asm("ADD ESP, 8")
        # print(self.children[0].evaluate(ST)[0])
        # return 0
    
########################################################################
class Scan(Node):
    def evaluate(self, ST):
        Writer.write_asm("PUSH scanint")
        Writer.write_asm("PUSH formatin")
        Writer.write_asm("call scanf")
        Writer.write_asm("ADD ESP, 8")
        Writer.write_asm("PUSH scanint")
        Writer.write_asm("MOV EAX, DWORD [scanint]")
        return (int(input()), "int")


class ForLoop(Node):
    def evaluate(self, ST):
        self.children[0].evaluate(ST)
        Writer.write_asm("LOOP_{}:".format(self.id))
        self.children[1].evaluate(ST)
        Writer.write_asm("CMP EAX, False")
        Writer.write_asm("JE EXIT_{}".format(self.id))
        self.children[3].evaluate(ST)
        self.children[2].evaluate(ST)
        Writer.write_asm("JMP LOOP_{}".format(self.id))
        Writer.write_asm("EXIT_{}:".format(self.id))
        # while self.children[1].evaluate(ST)[0]:
        #     self.children[3].evaluate(ST)
        #     self.children[2].evaluate(ST)
            
class IfCond(Node):
    def evaluate(self, ST):
        Writer.write_asm("IF_{}".format(self.id))
        self.children[0].evaluate(ST)
        Writer.write_asm("CMP EAX, False")
        Writer.write_asm("JE EXIT_{}".format(self.id))
        self.children[1].evaluate(ST)
        Writer.write_asm("JMP EXIT_{}".format(self.id))
        Writer.write_asm("EXIT_{}".format(self.id))
        
        if len(self.children) > 2:
            Writer.write_asm("ELSE_{}".format(self.id))
            self.children[2].evaluate(ST)
            Writer.write_asm("JMP EXIT_{}".format(self.id))
            Writer.write_asm("EXIT_{}".format(self.id))
        
        # if self.children[0].evaluate(ST):
        #     self.children[1].evaluate(ST)
        # elif (len(self.children)>2):
        #     self.children[2].evaluate(ST)
            
########################################################################
class VarDec(Node):
    def evaluate(self, ST):
        # if len(self.children) == 1:
        #     if self.value == "int":
        #         ST.create(self.children[0].value, (0, self.value))
        #     elif self.value == "string":
        #         ST.create(self.children[0].value, ("", self.value))
            
        # else:
        #     ST.create(self.children[0].value, (self.children[1].evaluate(ST)[0], self.value))
        Writer.write_asm("PUSH DWORD 0")
        ST.create(self.children[0].value, None, self.value)
            
            
class StrVal(Node):
    def evaluate(self, ST):
        return (self.value, "string")