import sys

def soma(operacao):
    operacao = operacao.replace(" ", "")
    sinais = ["+", "-"]
    lista = []
    numero_atual = ""
    
    for i in operacao:
        if i in sinais:
            if numero_atual != "":
                lista.append(numero_atual)
                numero_atual = ""
            else:
                return None
            lista.append(i)
        else:
            numero_atual += i
    
    if numero_atual != "":
        lista.append(numero_atual)
    
    if len(lista) < 3 or lista[0] in sinais or lista[len(lista)-1] in sinais:
        return None
    
    total = int(lista[0])
    print(lista)

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