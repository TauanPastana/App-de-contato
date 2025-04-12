from conexão import *
from contato import Contato

def menu():
    while True:
        try:
            print('Bem vindo ao seu app de contatos')
            print('Escolha uma das opções abaixo:')
            print('1 - Criar um novo contato')
            print('2 - Mostrar todos os contatos')
            print('3 - Buscar um nome')
            print('4 - Editar um contato')
            print('5 - Apagar um contato')
            print('6 - Finalizar')
            opc = int(input(': '))
            if opc == 1:
                contato = Contato()
                salvar_arquivo(contato.nome,contato.numero)
            elif opc == 2:
                selecao()
            elif opc == 3:
                verificacao(1)
            elif opc == 4:
                editar()
            elif opc == 5:
                verificacao(3)
            elif opc == 6:
                break
        except ValueError:
            print("Opção incorreta, tente novamente!")