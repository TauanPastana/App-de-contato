import psycopg2


conexao = psycopg2.connect(database="postgres",
                           host="localhost",
                           user="tauan_pastana",
                           password="600227",
                           port="5432")
PermissionError(conexao.status)


def commit():
    print('Deseja confirmar as alterações?\nDigite 1 para confimar\n2 Para não confrimar')
    opc = int(input(": "))
    if opc == 1:
        conexao.commit()
        from modulos_utils import clear
        clear()
        
    elif opc == 2:
        from menu import menu
        conexao.rollback()
        menu()
        
        





