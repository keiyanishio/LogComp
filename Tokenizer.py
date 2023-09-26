class Token:
    def __init__(self, t_type: str, value):
        self.t_type = t_type
        self.value = value

class Tokenizer:

    def __init__(self, source):
        self.source = source
        self.position = 0
        self.next = None
        
    
    
    def selectNext(self):
        #print((self.source))
    

        if self.position < len(self.source):
            current_char = self.source[self.position]
        
            #print(current_char)
            
            if current_char == '\n':
                self.next = Token('NEWLINE', '\n')
                self.position += 1
                
            elif current_char.isspace():
                self.position += 1
                self.selectNext()
                
            elif current_char.isalpha() or current_char == "_":
                identifier = ""
                while self.position < len(self.source) and (current_char.isalnum() or current_char == "_"):
                    identifier += current_char
                    self.position += 1
                    if self.position < len(self.source):
                        current_char = self.source[self.position]

                if identifier == "Println":
                    self.next = Token('PRINTLN', 'Println')
                    
                elif identifier == "Scanln":
                    self.next = Token('SCANLN', 'Scanln')
                    
                elif identifier == "if":
                    self.next = Token('IF', 'if')
                    
                elif identifier == "else":
                    self.next = Token('ELSE', 'else')
    
                else:
                    self.next = Token('IDENTIFIER', identifier)

            elif current_char.isdigit():
                value = ""
                while self.position < len(self.source) and self.source[self.position].isdigit():
                    value += self.source[self.position]
                    if self.source[self.position+1].isalpha():
                        raise SyntaxError("Erro: Caractere inválido")
                    #print(self.source[self.position+1])
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
                if self.source[self.position+1] == "=":
                    self.next = Token('EQUALCON', '==')
                    self.position += 2
                else:
                    self.next = Token('EQUAL', '=') 
                    self.position += 1
                
            elif current_char == ">":
                self.next = Token('GT', '>') 
                self.position += 1
                
            elif current_char == "<":
                self.next = Token('LT', '<') 
                self.position += 1
                
            elif current_char == "|":
                self.next = Token('OR', '||') 
                self.position += 2
                
            elif current_char == "&":
                self.next = Token('AND', '&&') 
                self.position += 2
                
            elif current_char == "!":
                self.next = Token('NOT', '!') 
                self.position += 1
                
            elif current_char == "{":
                self.next = Token('CHAVES_A', '{') 
                self.position += 1
            
        
            elif current_char == "}":
                self.next = Token('CHAVES_F', '}') 
                self.position += 1 
                
            elif current_char == ";":
                self.next = Token('PV', ';') 
                self.position += 1                
            
            else:
                raise SyntaxError("Erro: Caractere inválido")

        else:
            self.next = Token('EOF', 'EOF')
            