import sys
import re 
from Tokenizer import *
from AST import *
from SymbolTable import *

class PrePro:
    @staticmethod
    def filter(source):
        source = re.sub(r'\/\/[^\n]*', '', source) 
        source = re.sub(r'\/\*.*?\*\/', '', source, flags=re.DOTALL)  

        lines = source.split('\n')
        non_empty_lines = [line for line in lines if line.strip() != '']
        
        filtered_source = '\n'.join(non_empty_lines)

        return filtered_source.strip()

    


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
        else:
            raise SyntaxError("Erro: ERRO")

    
        #return NoOp(None, None)
                    
        
                
        
    
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
    
    
    
    

