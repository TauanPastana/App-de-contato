from conexao import conexao, commit
from modulos_utils import *
from tabulate import tabulate
from faker import Faker
faker = Faker("pt_BR")

def salvar_arquivo(nome, telefone):
    with conexao.cursor() as cursor:
        cursor.execute("INSERT INTO contato (nome, telefone) VALUES (%s, %s)", (nome, telefone))
        conexao.commit()
        print("\nContato criado!")
        clear()


def selecao():
    with conexao.cursor() as cursor:
        clear()
        cursor.execute("SELECT * FROM contato")
        resultado = cursor.fetchall()
        if resultado:
            cabecalho = ["ID", "Nome", "Telefone"]
            print(tabulate(resultado, headers=cabecalho, tablefmt="fancy_grid"))
        else:
            print('Não tem contato existente')


def verificacao(*args):
    with conexao.cursor() as cursor:
        busca = input("Digite o nome do contato: ").capitalize()
        busca = f"%{busca}%"
        cursor.execute("""SELECT * FROM contato 
                          WHERE nome LIKE %s""", (busca,))
        resultado = cursor.fetchall()

        if resultado:
            if 1 in args:
                clear()
                cabecalho = ["ID", "Nome", "Telefone"]
                print(tabulate(resultado, headers=cabecalho, tablefmt="fancy_grid"))
            elif 2 in args:
                return resultado
            elif 3 in args:
                clear()
                if len(resultado) == 1:
                    cabecalho = ["ID", "Nome", "Telefone"]
                    print(tabulate(resultado, headers=cabecalho, tablefmt="fancy_grid"))
                    id = resultado[0][0]
                    deletar(id)
                elif len(resultado) > 1:
                    cabecalho = ["ID", "Nome", "Telefone"]
                    print(tabulate(resultado, headers=cabecalho, tablefmt="fancy_grid"))
                    IDs = [valor[0] for valor in resultado]
                    try:
                        id = int(input("Digite o ID do contanto que deseja apagar\n: "))
                        if id in IDs:
                            deletar(id)
                        else:
                            print("ID não correspondente")
                            voltar(editar)
                    except ValueError:
                        print("Opção incorreta!")
                        voltar(editar)
        else:
            clear()
            print('Nome de contato não encontrado\n')
            from main import menu
            menu()
            


def deletar(id):
    with conexao.cursor() as cursor:
        print("Deseja realmente excluir?\n1 para confirmar\n2 para voltar")
        opc = int(input(": "))
        if opc == 1:
            cursor.execute("""DELETE
                              FROM contato
                              WHERE id = %s""", (id,))
            commit()
        elif opc == 2:
            voltar()


def editar():
    resultados = verificacao(2)
    if len(resultados) == 1:
        print("Contato encontrado")
        cabecalho = ["ID", "Nome", "Telefone"]
        print(tabulate(resultados, headers=cabecalho, tablefmt="fancy_grid"))
        editar_1(resultados[0][0])
    elif len(resultados) > 1:
        cabecalho = ["ID", "Nome", "Telefone"]
        print(tabulate(resultados, headers=cabecalho, tablefmt="fancy_grid"))
        IDs = [linha[0] for linha in resultados]
        try:
            opc = int(input("Digite o ID do contanto que deseja editar\n: "))
            if opc in IDs:
                editar_1(id=opc)
            else:
                print("ID não correspondente")
                voltar(editar)
        except ValueError:
            print("Opção incorreta!")
            voltar(editar)
    else:
        print("Contato não encontrado!")
        voltar(editar)


def editar_1(id):
    with conexao.cursor() as cursor:
        
        print('Digite 1 para editar o nome\nDigite 2 para editar o telefone\nDigite 3 para editar ambos')
        try:
            opc = int(input(': '))
            clear()
            if opc == 1:
                nome = input("Digite seu nome: ")
                nome = maiscula(nome)
                cursor.execute("""UPDATE contato 
                                  SET nome = %s 
                                  WHERE id = %s""", (nome, id))
                print("Contato renomeado\n")
                commit()
            elif opc == 2:
                telefone = int(input("Digite seu telefone: "))
                cursor.execute("""UPDATE contato 
                                  SET telefone = %s 
                                  WHERE id = %s""", (telefone, id))
                print("Contato renomeado")
                commit()
            elif opc == 3:
                nome = input("Digite seu nome: ").capitalize()
                nome = maiscula(nome)
                telefone = int(input("Digite seu telefone: "))
                cursor.execute("""UPDATE contato 
                                  SET nome = %s, telefone = %s 
                                  WHERE id = %s""", (nome, telefone, id,))
                commit()
            else:
                print("Opção inexistente")
                voltar(editar)
        except ValueError:
            print("Opção inválida")
            voltar(editar)






def names_generate():  
    
    lista = []
    for i in range(20): 
        tupla = (faker.name(),faker.phone_number())
        lista.append(tupla)
    return lista

def contatc_automatic():
    with conexao.cursor() as cursor:
        try:
            lista = names_generate()
            query = "INSERT INTO contato (nome, telefone) VALUES (%s, %s)"
            cursor.executemany(query,lista)
            print("Dados fakes gerados com sucessos!")
        except Exception as e:
            conexao.rollback()