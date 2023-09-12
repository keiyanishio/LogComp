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
        return source[:i]
            
        

class Tokenizer:

    def __init__(self, source):
        self.source = source.replace(" ", "").strip()
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
                
                

            else:
                raise SyntaxError("Erro: Caractere inválido")

        else:
            self.next = Token('EOF', '')

class Node:
    def __init__(self, value, children):
        self.value = value 
        self.children = children
        

    def evaluate(self):
        None
    
class BinOp(Node):
    def evaluate(self):
        if self.value == "+":
            return self.children[0].evaluate() + self.children[1].evaluate()
        
        elif self.value == "-":
            return self.children[0].evaluate() - self.children[1].evaluate()
        
        elif self.value == "*":
            return self.children[0].evaluate() * self.children[1].evaluate()
        
        elif self.value == "/":
            return self.children[0].evaluate() // self.children[1].evaluate()

class UnOp(Node):
    def evaluate(self):
        if self.value == "+":
            return self.children[0].evaluate()
        else:
            return -self.children[0].evaluate()
        
class IntVal(Node):
    def evaluate(self):
        return self.value

class NoOp(Node):
    def evaluate(self):
        return None
        


class Parser:
    tokenizer = None
    
    def factor(self):
        self.tokenizer.selectNext()
        
        if self.tokenizer.next.t_type == 'INT':
            result = self.tokenizer.next.value
            self.tokenizer.selectNext()
            res = IntVal(result, [])
            return res
            
        elif self.tokenizer.next.t_type == 'PLUS':
            return UnOp("+", [self.factor()])
        
        elif self.tokenizer.next.t_type == 'MINUS':
            return UnOp("-", [self.factor()])
        
        elif self.tokenizer.next.t_type == 'OPEN':
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
        #print(result)
        while self.tokenizer.next.t_type == 'PLUS' or self.tokenizer.next.t_type == 'MINUS':
            op = self.tokenizer.next
            num = self.parser_term()
            if op.t_type == 'PLUS':
                result = BinOp(op.value, [result, num])
            elif op.t_type == 'MINUS':
                result = BinOp(op.value, [result, num])
                   
        return result
    
    
    
    def parser_term(self):
        result = self.factor()
        #print(result)
        while self.tokenizer.next.t_type == 'MULTI' or self.tokenizer.next.t_type == 'DIV':
            op = self.tokenizer.next
            num = self.factor()
            if op.t_type == 'MULTI':
                result = BinOp(op.value, [result, num])
            elif op.t_type == 'DIV':
                result = BinOp(op.value, [result, num])
                   
        return result
        
            


    def run(self, code):
        pre_processo = PrePro.filter(code)
        Parser.tokenizer = Tokenizer(pre_processo)
        result = self.parser_expression()
        if self.tokenizer.next.t_type != 'EOF':
            raise SyntaxError("EOFFFFFFF")
        return result


    
if __name__ == "__main__":
    p = Parser()
    file = sys.argv[1]
    with open(file, 'r') as arquivo:
        conteudo = arquivo.read()
    arquivo.close()
    
    #print("Input Content:")
    #print(conteudo)
    teste = p.run(conteudo)
    result = teste.evaluate()
    print(result)
    
    
    

