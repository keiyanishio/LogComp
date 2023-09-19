import sys


class Token:
    def __init__(self, t_type: str, value):
        self.t_type = t_type
        self.value = value

class PrePro:
    @staticmethod
    def filter(source):
        i = 0 
        while i < len(source):
            if source[i:i+2] == "//":
                break
            i += 1
        return source[:i].replace(" ", "").strip()
            
        

class Tokenizer:

    def __init__(self, source):
        self.source = source
        self.position = 0
        self.next = None
    
    
    def selectNext(self):
        #print((self.source))
        if len(self.source) <= 2:
            raise SyntaxError("Erro: Caractere inválido")
        if self.position < len(self.source):
            current_char = self.source[self.position]

            if current_char.isdigit():
                value = ""
                while self.position < len(self.source) and self.source[self.position].isdigit():
                    value += self.source[self.position]
                    self.position += 1
                self.next = Token('INT', int(value))
                
            elif current_char == "*":
                self.next = Token('MULTI', '*')
                self.position += 1

            elif current_char == "/":
                self.next = Token('DIV', '/') 
                self.position += 1

            elif current_char == "+":
                self.next = Token('PLUS', '+')
                self.position += 1

            elif current_char == "-":
                self.next = Token('MINUS', '-') 
                self.position += 1
                
            elif current_char == "(":
                self.next = Token('OPEN', '(') 
                self.position += 1
            
            elif current_char == ")":
                self.next = Token('CLOSE', ')') 
                self.position += 1
                
            elif current_char == "=":
                self.next = Token('EQUAL', '=') 
                self.position += 1
            
            elif current_char.isalpha():
                identifier = ""
                while self.position < len(self.source) and self.source[self.position].isalnum():
                    identifier += self.source[self.position]
                    self.position += 1

                if identifier == "Println":
                    self.next = Token('PRINTLN', 'Println')
                else:
                    self.next = Token('IDENTIFIER', identifier)
                    
            elif current_char == '\n':
                self.next = Token('NEWLINE', '\n')
                self.position += 1
                

            else:
                raise SyntaxError("Erro: Caractere inválido")

        else:
            self.next = Token('EOF', 'EOF')
            
            
class SymbolTable:
    def __init__(self):
        self.table = {}

    def setter(self, key, value):
        self.table[key] = value
        
    def getter(self, key):
        return self.table[key]
    

    

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






class Parser:
    tokenizer = None
    
    def block(self):
        children = []
        #self.tokenizer.selectNext()
        while self.tokenizer.next.t_type != 'EOF':
            children.append(self.statement())
            #self.tokenizer.selectNext()
        return Block(None, children)
    
    def statement(self):
        if self.tokenizer.next.t_type == 'IDENTIFIER':
            identi = Identifier(self.tokenizer.next.value, [])
            self.tokenizer.selectNext()
            if self.tokenizer.next.t_type == 'EQUAL':
                self.tokenizer.selectNext()
                result = Assigment(None, [identi, self.parser_expression()])
                #print(self.tokenizer.next.value)
                if self.tokenizer.next.t_type == 'NEWLINE':
                    self.tokenizer.selectNext()
                    return result
                elif self.tokenizer.next.t_type == 'EOF':
                    return result
                else:
                    #print(repr(self.tokenizer.next.value))
                    raise SyntaxError("Erro: NEWLINE IDENTIFIER")
            else:
                raise SyntaxError("Erro: EQUAL")

        elif self.tokenizer.next.t_type == 'PRINTLN':
            self.tokenizer.selectNext()
            if self.tokenizer.next.t_type == 'OPEN':
                self.tokenizer.selectNext()
                #print(self.tokenizer.next.value)
                result = self.parser_expression()
                #print(result.value)
                if self.tokenizer.next.t_type == 'CLOSE':
                    self.tokenizer.selectNext()
                    final = Print(None, [result]) 
                    if self.tokenizer.next.t_type == 'NEWLINE':
                        self.tokenizer.selectNext()
                        return final
                    elif self.tokenizer.next.t_type == 'EOF':
                        return final
                    else:
                        raise SyntaxError("Erro: NEWLINE PRINTLN")
                else:
                    raise SyntaxError("Erro: CLOSE")
            else:
                raise SyntaxError("Erro: OPEN")

        elif self.tokenizer.next.t_type == 'NEWLINE' or self.tokenizer.next.t_type == 'EOF':
            result = NoOp(None, None)
            return result

    
        return NoOp(None, None)
                    
        
                
        
    
    def factor(self):
        
        #self.tokenizer.next.t_type
        if self.tokenizer.next.t_type == 'INT':
            result = self.tokenizer.next.value
            self.tokenizer.selectNext()
            res = IntVal(result, [])
            return res
        
        elif self.tokenizer.next.t_type == "IDENTIFIER":
            result = self.tokenizer.next.value
            identi = Identifier(result, [])
            self.tokenizer.selectNext()
            return identi
        
        elif self.tokenizer.next.t_type == 'PLUS':
            self.tokenizer.selectNext()
            return UnOp("+", [self.factor()])
        
        elif self.tokenizer.next.t_type == 'MINUS':
            self.tokenizer.selectNext()
            return UnOp("-", [self.factor()])
        
        elif self.tokenizer.next.t_type == 'OPEN':
            self.tokenizer.selectNext()
            result = self.parser_expression()
            if self.tokenizer.next.t_type == 'CLOSE':
                self.tokenizer.selectNext()
                return result
            else:
                raise SyntaxError("Erro: Caractere inválido")
        else:
            raise SyntaxError("Erro: Caractere inválido")
            
        
        
    
    def parser_expression(self):
        result = self.parser_term()
        #print(result.value)
        while self.tokenizer.next.t_type == 'PLUS' or self.tokenizer.next.t_type == 'MINUS':
            op = self.tokenizer.next
            if op.t_type == 'PLUS':
                self.tokenizer.selectNext()
                result = BinOp(op.value, [result, self.parser_term()])
            elif op.t_type == 'MINUS':
                self.tokenizer.selectNext()
                result = BinOp(op.value, [result, self.parser_term()])
                   
        return result
    
    
    
    def parser_term(self):
        result = self.factor()
        #print(result)
        while self.tokenizer.next.t_type == 'MULTI' or self.tokenizer.next.t_type == 'DIV':
            op = self.tokenizer.next
            
            if op.t_type == 'MULTI':
                self.tokenizer.selectNext()
                result = BinOp(op.value, [result, self.factor()])
            elif op.t_type == 'DIV':
                self.tokenizer.selectNext()
                result = BinOp(op.value, [result, self.factor()])
                   
        return result
        
            


    def run(self, code):
        pre_processo = PrePro.filter(code)
        Parser.tokenizer = Tokenizer(pre_processo)
        self.tokenizer.selectNext()
        result = self.block()
        if self.tokenizer.next.t_type != 'EOF':
            raise SyntaxError("EOFFFFFFF")
        return result


    
if __name__ == "__main__":
    ST = SymbolTable()
    p = Parser()
    file = sys.argv[1]
    with open(file, 'r') as arquivo:
        conteudo = arquivo.read()
    arquivo.close()
    
    #print("Input Content:")
    #print(repr(conteudo))
    
    teste = p.run(conteudo)
    teste.evaluate(ST)
    #print(ST.table)
    
    
    
    

