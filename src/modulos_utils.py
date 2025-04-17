

def maiscula(nome: str):
    nome_separador = nome.split(" ")
    nome_separador = [nome.capitalize() for nome in nome_separador]
    nome_capitalize = " ".join(nome_separador)
    return nome_capitalize

def clear():
    import os
    os.system('cls') or None

def voltar(func, numero = None):
    
    print("Digite 1 para voltar\nDigite 2 para voltar para o menu principal")
    opc = int(input(': '))
    if opc == 1:
        func(numero)
    elif opc == 2:
        from main import menu
        menu()