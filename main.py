import sys
import re 
from Tokenizer import *
from AST import *
from SymbolTable import *
from FuncTable import *


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
    
    def parseProgram(self):
        children = []
        while self.tokenizer.next.t_type != 'EOF':
            children.append(self.parseDeclaration())
        children_main = FuncCall("main", [])
        children.append(children_main)
        return Block(None, children)
    
    
    def parseDeclaration(self):
        
        while self.tokenizer.next.t_type == 'NEWLINE':
            self.tokenizer.selectNext()
        
        if self.tokenizer.next.t_type == 'FUNC':
            self.tokenizer.selectNext()
            result = FuncDec(None, [])
            if self.tokenizer.next.t_type == 'IDENTIFIER':
                func_name = Identifier(self.tokenizer.next.value, [])
                self.tokenizer.selectNext()
                
                if self.tokenizer.next.t_type == 'OPEN':
                    self.tokenizer.selectNext()
                    if self.tokenizer.next.t_type == 'CLOSE':
                        self.tokenizer.selectNext()
                        if self.tokenizer.next.t_type == 'TYPE':
                            func_type = self.tokenizer.next.value
                            self.tokenizer.selectNext()
                            block = self.parseBlock()
                            var_name = VarDec(func_type, [func_name])
                        
                            return FuncDec(None, [var_name, block])
                            
                            
                    elif self.tokenizer.next.t_type == 'IDENTIFIER':
                        
                        arg = Identifier(self.tokenizer.next.value, [])
                        self.tokenizer.selectNext()
                        if self.tokenizer.next.t_type == 'TYPE':
                            tipo = self.tokenizer.next.value
                            result.children.append(VarDec(tipo, [arg]))
                            self.tokenizer.selectNext()
                            
                            while self.tokenizer.next.t_type == 'VIRGULA':
                                self.tokenizer.selectNext()
                                if self.tokenizer.next.t_type == 'IDENTIFIER':
                                    arg = Identifier(self.tokenizer.next.value, [])
                                    self.tokenizer.selectNext()
                                    if self.tokenizer.next.t_type == 'TYPE':
                                        tipo = self.tokenizer.next.value
                                        result.children.append(VarDec(tipo, [arg]))
                                        self.tokenizer.selectNext()
                                    
                            if self.tokenizer.next.t_type == 'CLOSE':
                                self.tokenizer.selectNext()
                                if self.tokenizer.next.t_type == 'TYPE':
                                    func_type = self.tokenizer.next.value
                                    self.tokenizer.selectNext()
                                    block = self.parseBlock()
                                    result.children.append(block)
                                    var_name = VarDec(func_type, [func_name])
                                    result.children.insert(0, var_name)
                                    return result
        else:
            raise SyntaxError("Erro: Precisa de função")
    
    def parseBlock(self):
        command = []
        if self.tokenizer.next.t_type == 'CHAVES_A':
            self.tokenizer.selectNext()
            
            if self.tokenizer.next.t_type == 'NEWLINE':
                self.tokenizer.selectNext()
                while self.tokenizer.next.t_type != 'CHAVES_F':
                    command.append(self.parseStatement())
            else:
                raise SyntaxError("Erro: Abre Chaves no IF")
            self.tokenizer.selectNext()
        return Block(None, command)
    
    
    
    def parseAssigments(self):
        args = []
        if self.tokenizer.next.t_type == 'IDENTIFIER':
            identi = Identifier(self.tokenizer.next.value, [])
            self.tokenizer.selectNext()
            
            if self.tokenizer.next.t_type == 'EQUAL':
                self.tokenizer.selectNext()
                result = Assigment(None, [identi, self.parseBoolExpression()])
                if self.tokenizer.next.t_type == 'IDENTIFIER' or self.tokenizer.next.t_type == 'VIRGULA' or self.tokenizer.next.t_type == 'CLOSE':
                    raise SyntaxError("Erro: Assigment")
                return result
            elif self.tokenizer.next.t_type == 'OPEN':
                self.tokenizer.selectNext()
                
                if self.tokenizer.next.t_type != 'CLOSE':
                    arg = self.parseBoolExpression()
                    args.append(arg)
                    while self.tokenizer.next.t_type == 'VIRGULA':
                        self.tokenizer.selectNext()
                        arg = self.parseBoolExpression()
                        args.append(arg)
                    
                    if self.tokenizer.next.t_type == 'CLOSE':
                        self.tokenizer.selectNext()
                        return FuncCall(identi.value, args)
                    else:
                        raise SyntaxError("Erro: fecha funccall")
                elif self.tokenizer.next.t_type == 'CLOSE':
                    self.tokenizer.selectNext()
                    return FuncCall(identi.value, [])
                else:
                    raise SyntaxError("Erro: fecha funccall")
            else:
                raise SyntaxError("Erro: fecha funccall")
                    
            
                    
    def parseStatement(self):
        if self.tokenizer.next.t_type == 'IDENTIFIER':
            assign = self.parseAssigments()
            self.tokenizer.selectNext()
            return assign

        elif self.tokenizer.next.t_type == 'PRINTLN':
            self.tokenizer.selectNext()
            if self.tokenizer.next.t_type == 'OPEN':
                self.tokenizer.selectNext()
                result = self.parseBoolExpression()
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
            
            
        elif self.tokenizer.next.t_type == "IF":
            self.tokenizer.selectNext()
            condi = self.parseBoolExpression()
            block_if = self.parseBlock()
            if self.tokenizer.next.t_type == "ELSE":
                self.tokenizer.selectNext()
                block_else = self.parseBlock()
                if self.tokenizer.next.t_type == "NEWLINE" or self.tokenizer.next.t_type == "EOF":
                    self.tokenizer.selectNext()
                    if self.tokenizer.next.t_type == "CHAVES_A":
                        raise SyntaxError("Erro: Sintaxe no else")
                    return IfCond(None, [condi, block_if, block_else])
            elif self.tokenizer.next.t_type == "EOF" or self.tokenizer.next.t_type == "NEWLINE":
                self.tokenizer.selectNext()
                if self.tokenizer.next.t_type == "ELSE" or self.tokenizer.next.t_type == "CHAVES_A":
                    raise SyntaxError("Erro: Sintaxe no if ")
                return IfCond(None, [condi, block_if])        
            else:
                raise SyntaxError("Erro: IDENTAÇÃO")
        
        
        
        
        elif self.tokenizer.next.t_type == 'FOR':
            self.tokenizer.selectNext()
            init = self.parseAssigments()
            if self.tokenizer.next.t_type == 'PV':
                self.tokenizer.selectNext()
                condition = self.parseBoolExpression()
                if self.tokenizer.next.t_type == 'PV':
                    self.tokenizer.selectNext()
                    inc = self.parseAssigments()
                    block_for = self.parseBlock()
                    if self.tokenizer.next.t_type == 'NEWLINE':
                        self.tokenizer.selectNext()
                        return ForLoop("for", [init, condition, inc, block_for])
                    elif self.tokenizer.next.t_type == 'EOF':
                        return ForLoop("for", [init, condition, inc, block_for])
                    else:
                        #print(repr(self.tokenizer.next.value))
                        raise SyntaxError("Erro: NEWLINE IDENTIFIER")
                                                
        
            else:
                raise SyntaxError("Erro: init for")

        
        
        elif self.tokenizer.next.t_type == 'VAR':
            self.tokenizer.selectNext()
            if self.tokenizer.next.t_type == 'IDENTIFIER':
                identi = Identifier(self.tokenizer.next.value, [])
                self.tokenizer.selectNext()
                if self.tokenizer.next.t_type == 'TYPE':
                    tipo = self.tokenizer.next.value 
                    decvar = VarDec(tipo, [identi])
                    self.tokenizer.selectNext()
                    if self.tokenizer.next.t_type == 'EQUAL':
                        self.tokenizer.selectNext()
                        result = VarDec(tipo, [identi, self.parseBoolExpression()])
                        if self.tokenizer.next.t_type == 'NEWLINE' or self.tokenizer.next.t_type == 'EOF':
                            #print(self.tokenizer.next.t_type)
                            self.tokenizer.selectNext()
                            return result
                    elif self.tokenizer.next.t_type == 'NEWLINE' or self.tokenizer.next.t_type == 'EOF':
                        self.tokenizer.selectNext()
                        return decvar
                    else:
                        raise SyntaxError("Erro: Na hora de declarar")
                        
                           
        
        elif self.tokenizer.next.t_type == 'RETURN':
            self.tokenizer.selectNext()
            final = ReturnNode(None, [self.parseBoolExpression()])
            if self.tokenizer.next.t_type == 'NEWLINE':
                self.tokenizer.selectNext()
                return final
            
        elif self.tokenizer.next.t_type == 'NEWLINE' or self.tokenizer.next.t_type == 'EOF':
            result = NoOp(None, None)
            return result
        else:
            raise SyntaxError("Erro: caracter errado")
        
                
        
    
    def parseFactor(self):
        
        if self.tokenizer.next.t_type == 'INT':
            result = self.tokenizer.next.value
            self.tokenizer.selectNext()
            res = IntVal(result, [])
            return res
        
        elif self.tokenizer.next.t_type == 'STRING':
            result = self.tokenizer.next.value
            self.tokenizer.selectNext()
            string = StrVal(result, [])
            return string
        
        elif self.tokenizer.next.t_type == "IDENTIFIER":
            result = self.tokenizer.next.value
            identi = Identifier(result, [])
            self.tokenizer.selectNext()
            if self.tokenizer.next.t_type == 'OPEN':
                res = FuncCall(identi.value, [])
                self.tokenizer.selectNext()
                
                if self.tokenizer.next.t_type != 'CLOSE':
                    arg = self.parseBoolExpression()
                    res.children.append(arg)
                    while self.tokenizer.next.t_type == 'VIRGULA':
                        self.tokenizer.selectNext()
                        arg = self.parseBoolExpression()
                        res.children.append(arg)
                    
                    if self.tokenizer.next.t_type == 'CLOSE':
                        self.tokenizer.selectNext()
                        return res
                    
                else:
                    self.tokenizer.selectNext()
                    return res
            else:
                return identi
    
        
        elif self.tokenizer.next.t_type == 'PLUS':
            self.tokenizer.selectNext()
            return UnOp("+", [self.parseFactor()])
        
        elif self.tokenizer.next.t_type == 'MINUS':
            self.tokenizer.selectNext()
            return UnOp("-", [self.parseFactor()])
        
        elif self.tokenizer.next.t_type == 'NOT':
            self.tokenizer.selectNext()
            return UnOp("!", [self.parseFactor()])
        
        
        elif self.tokenizer.next.t_type == "SCANLN":
            self.tokenizer.selectNext()
            if self.tokenizer.next.t_type == 'OPEN':
                self.tokenizer.selectNext()
                if self.tokenizer.next.t_type == 'CLOSE':
                    self.tokenizer.selectNext()
                    if self.tokenizer.next.t_type == 'NEWLINE':
                        return Scan("Scanln", [])
                else:
                    raise SyntaxError("Erro: Caractere inválido")
        
        elif self.tokenizer.next.t_type == 'OPEN':
            self.tokenizer.selectNext()
            result = self.parseBoolExpression()
            if self.tokenizer.next.t_type == 'CLOSE':
                self.tokenizer.selectNext()
                return result
            else:
                raise SyntaxError("Erro: Caractere inválido")
            
        
        else:
            raise SyntaxError("Erro: Caractere inválido")
            
        
        
    
    def parseExpression(self):
        result = self.parseTerm()
        #print(result.value)
        while self.tokenizer.next.t_type == 'PLUS' or self.tokenizer.next.t_type == 'MINUS' or self.tokenizer.next.t_type == 'CONCAT':
            op = self.tokenizer.next
            if op.t_type == 'PLUS':
                self.tokenizer.selectNext()
                result = BinOp(op.value, [result, self.parseTerm()])
            elif op.t_type == 'MINUS':
                self.tokenizer.selectNext()
                result = BinOp(op.value, [result, self.parseTerm()])

            elif op.t_type == 'CONCAT':
                self.tokenizer.selectNext()
                result = BinOp(op.value, [result, self.parseTerm()])
                   
        return result
    
    
    
    def parseTerm(self):
        result = self.parseFactor()
        #print(result)
        while self.tokenizer.next.t_type == 'MULTI' or self.tokenizer.next.t_type == 'DIV':
            op = self.tokenizer.next
            
            if op.t_type == 'MULTI':
                self.tokenizer.selectNext()
                result = BinOp(op.value, [result, self.parseFactor()])
            elif op.t_type == 'DIV':
                self.tokenizer.selectNext()
                result = BinOp(op.value, [result, self.parseFactor()])
                   
        return result
    
    def parseBoolExpression(self):
        result = self.parseBoolTerm()
        #print(result)
        while self.tokenizer.next.t_type == 'OR':
            op = self.tokenizer.next
            self.tokenizer.selectNext()
            result = BinOp(op.value, [result, self.parseBoolTerm()])
                   
        return result
    
    def parseBoolTerm(self):
        result = self.parseRelExpression()
        #print(result)
        while self.tokenizer.next.t_type == 'AND':
            op = self.tokenizer.next
            self.tokenizer.selectNext()
            result = BinOp(op.value, [result, self.parseRelExpression()])
                   
        return result
    
    
    def parseRelExpression(self):
        result = self.parseExpression()
        #print(result)
        while self.tokenizer.next.t_type == 'EQUALCON' or self.tokenizer.next.t_type == 'GT' or self.tokenizer.next.t_type == 'LT':
            op = self.tokenizer.next
            
            if op.t_type == 'EQUALCON':
                self.tokenizer.selectNext()
                result = BinOp(op.value, [result, self.parseExpression()])
            elif op.t_type == 'GT':
                self.tokenizer.selectNext()
                result = BinOp(op.value, [result, self.parseExpression()])
            elif op.t_type == 'LT':
                self.tokenizer.selectNext()
                result = BinOp(op.value, [result, self.parseExpression()])
                   
        return result
        
    
            


    def run(self, code):
        pre_processo = PrePro.filter(code)
        Parser.tokenizer = Tokenizer(pre_processo)
        self.tokenizer.selectNext()
        result = self.parseProgram()
        if self.tokenizer.next.t_type != 'EOF':
            raise SyntaxError("EOFFFFFFF")
        return result


    
if __name__ == "__main__":
    ST = SymbolTable()
    FT = FuncTable()
    p = Parser()
    file = sys.argv[1]
    with open(file, 'r') as arquivo:
        conteudo = arquivo.read()+'\n'
    arquivo.close()
    
    #print("Input Content:")
    #print(repr(conteudo))
    teste = p.run(conteudo)
    teste.evaluate(ST)
    #print(FT.table)