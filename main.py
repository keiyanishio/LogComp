import sys

class Token:
    def __init__(self, t_type: str, value):
        self.t_type = t_type
        self.value = value

class Tokenizer:
    def __init__(self, source):
        self.source = source.replace(" ", "").strip()
        self.position = 0
        self.next = None
    
    
    def selectNext(self):
        #print(len(self.source))
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
        
        
class Parser:
    tokenizer = None
    
    def factor(self):
        #num = 0
        if self.tokenizer.next.t_type == 'INT':
            result = self.tokenizer.next.value
            self.tokenizer.selectNext()
            return result
            
        elif (self.tokenizer.next.t_type == 'PLUS' or self.tokenizer.next.t_type == 'MINUS'):
            result = self.factor()
            self.tokenizer.selectNext()
            return result
        
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
            
            
        #     while self.tokenizer.next.t_type == 'MULTI' or self.tokenizer.next.t_type == 'DIV':
        #         if self.tokenizer.next.value == '*':
        #             self.tokenizer.selectNext()
        #             num = self.tokenizer.next.value
        #             if isinstance(num, int):
        #                 result *= num
        #             else:
        #                 raise SyntaxError("Erro: Caractere inválido")
        #         if self.tokenizer.next.value == '/':
        #             self.tokenizer.selectNext()
        #             num = self.tokenizer.next.value
        #             if isinstance(num, int):
        #                 result //= num
        #             else:
        #                 raise SyntaxError("Erro: Caractere inválido")
        #         self.tokenizer.selectNext()
        #     return result
        # else:
        #     raise SyntaxError("Erro: Caractere inválido")
        
        
    
    def parser_expression(self):
        result = self.parser_term()
        #print(result)
        while self.tokenizer.next.t_type == 'PLUS' or self.tokenizer.next.t_type == 'MINUS':
            op = self.tokenizer.next
            self.tokenizer.selectNext()
            num = self.parser_term()
            if op.t_type == 'PLUS':
                result += num
            elif op.t_type == 'MINUS':
                result -= num
                   
        return result
    
    
    
    def parser_term(self):
        result = self.factor()
        #print(result)
        while self.tokenizer.next.t_type == 'MULTI' or self.tokenizer.next.t_type == 'DIV':
            op = self.tokenizer.next
            self.tokenizer.selectNext()
            num = self.factor()
            if op.t_type == 'MULTI':
                result *= num
            elif op.t_type == 'DIV':
                result //= num
                   
        return result
    
    
        # num = 0
        # if (self.tokenizer.next.t_type == 'INT' and flag_num == 0):
        #     result = self.tokenizer.next.value
        #     self.tokenizer.selectNext()
        #     while self.tokenizer.next.t_type == 'MULTI' or self.tokenizer.next.t_type == 'DIV':
        #         if self.tokenizer.next.value == '*':
        #             self.tokenizer.selectNext()
        #             num = self.tokenizer.next.value
        #             if isinstance(num, int):
        #                 result *= num
        #                 flag_num = 0
        #             else:
        #                 raise SyntaxError("Erro: Caractere inválido")
        #         if self.tokenizer.next.value == '/':
        #             self.tokenizer.selectNext()
        #             num = self.tokenizer.next.value
        #             if isinstance(num, int):
        #                 result //= num
        #                 flag_num = 0
        #             else:
        #                 raise SyntaxError("Erro: Caractere inválido")
        #         self.tokenizer.selectNext()
        #     return result
        # else:
        #     raise SyntaxError("Erro: Caractere inválido")
        
    
            


    def run(self, code):
        Parser.tokenizer = Tokenizer(code)
        Parser.tokenizer.selectNext()
        return self.parser_expression()
    
    
if __name__ == "__main__":
    p = Parser()
    teste = p.run(sys.argv[1])
    print(teste)
    