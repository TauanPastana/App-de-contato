import psycopg2
from tabulate import tabulate

conexao = psycopg2.connect(database="postgres",
                           host="localhost",
                           user="tauan_pastana",
                           password="600227",
                           port="5432")
PermissionError(conexao.status)


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
                cabecalho = ["ID", "Nome", "Telefone"]
                print(tabulate(resultado, headers=cabecalho, tablefmt="fancy_grid"))
            elif 2 in args:
                return resultado
            elif 3 in args:
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
            print('Nome de contato não encontrado')
            # from main import menu
            # menu()
            voltar(verificacao)


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


def voltar(func):
    clear()
    print("Digite 1 para voltar\nDigite 2 para voltar para o menu principal")
    opc = int(input(': '))
    if opc == 1:
        func(1)
    elif opc == 2:
        from main import menu
        menu()


def commit():
    print('Deseja confirmar as alterações?\nDigite 1 para confimar\n2 Para não confrimar')
    opc = int(input(": "))
    if opc == 1:
        conexao.commit()
        from main import menu
        menu()
    elif opc == 2:
        from main import menu
        menu()


def maiscula(nome: str):
    nome_separador = nome.split(" ")
    nome_separador = [nome.capitalize() for nome in nome_separador]
    nome_capitalize = " ".join(nome_separador)
    return nome_capitalize


def clear():
    import os
    os.system('cls') or None
