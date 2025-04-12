from conexão import maiscula
class Contato():
    def __init__(self):

        self.nome = input("Digite seu nome: ")
        self.nome = maiscula(self.nome)
        try:
            self.numero = int(input('Digite seu numero de telefone: '))
        except ValueError:
            print('Incorreto! Digite apenas números')

    
        

        
        
    