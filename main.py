import sys 
import re 

def soma (operacao):
    tira_espaco = operacao.replace(" ", "")
    lista = re.findall(r'\d+|[+\-]', tira_espaco)
    total = int(lista[0])
    
            
    i = 1
    while i < len(lista):
        if lista[i] == '-':
            total -= int(lista[i + 1])
        else:
            total += int(lista[i + 1])
        i += 2  
    
    print(total)
    return total
    
    

if __name__ == "__main__":
    soma(sys.argv[1])
    
    