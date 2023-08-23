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
        if self.position < len(self.source):
            current_char = self.source[self.position]

            if current_char.isdigit():
                value = ""
                while self.position < len(self.source) and self.source[self.position].isdigit():
                    value += self.source[self.position]
                    self.position += 1
                self.next = Token('INT', int(value))

            elif current_char == "+":
                self.next = Token('PLUS', '+')
                self.position += 1

            elif current_char == "-":
                self.next = Token('MINUS', '-') 
                self.position += 1
                

            else:
                raise SyntaxError("Erro: Caractere inválido")

        else:
            self.next = Token('EOF', '')
        
        
class Parser:
    tokenizer = None
    def parseExpression(self):
        flag_num = 0
        num = 0
        result = self.tokenizer.selectNext()
        if self.tokenizer.next.t_type == 'INT' and flag_num == 0:
            result = self.tokenizer.next.value
            #print(result)
            self.tokenizer.selectNext()
            flag_num = 1
            while self.tokenizer.next.t_type == 'PLUS' or self.tokenizer.next.t_type == 'MINUS':
                if self.tokenizer.next.value == '+':
                    self.tokenizer.selectNext()
                    num = self.tokenizer.next.value
                    if isinstance(num, int):
                        result += num
                        flag_num = 0
                    else:
                        raise SyntaxError("Erro: Caractere inválido")
                if self.tokenizer.next.value == '-':
                    self.tokenizer.selectNext()
                    num = self.tokenizer.next.value
                    if isinstance(num, int):
                        result -= num
                        flag_num = 0
                    else:
                        raise SyntaxError("Erro: Caractere inválido")
                self.tokenizer.selectNext()
            if flag_num == 1:
                raise SyntaxError("Erro: Caractere inválido")
            return result
        else:
            raise SyntaxError("Erro: Caractere inválido")
            


    def run(self, code):
        Parser.tokenizer = Tokenizer(code)
        return self.parseExpression()
if __name__ == "__main__":
    p = Parser()
    teste = p.run(sys.argv[1])
    print(teste)
    




