import random
from socket import *

grade = [[0,0,0],[0,0,0],[0,0,0]]
fim = False
print("+---------------------------------------------+")
print("|          Servidor Jogo da Velha             |")
print("+---------------------------------------------+")
print("Esperando conexão de cliente")

serverPort = 1200 
serverSocket = socket(AF_INET,SOCK_STREAM)

serverSocket.bind(("",serverPort))
serverSocket.listen(5)

connectionSocket, addr = serverSocket.accept()      #Espera cliente

def Desenha():
    ln = 0 
    
    print ("   | 1 | 2 | 3 | ")
        
    for linha in grade:
        print (" --+---+---+---+--")
        ln = ln +1
        linhaCompleta = " "+ str(ln) + " "
        for valor in linha:
            if  valor == 1:
                linhaCompleta = linhaCompleta + "| O "
            elif  valor == 2:
                linhaCompleta = linhaCompleta + "| X "
            else:
                linhaCompleta = linhaCompleta + "|   "
            
        linhaCompleta = linhaCompleta + "| "
        print (linhaCompleta)
        
    print (" --+---+---+---+--")
    print ("   |   |   |   | ")
    print ("\n")

def RespostaAi():
    global grade
    decidido = False
    i = 0
    j = 0
    
    i = random.randrange(3)
    j = random.randrange(3)
    
    while not decidido:
        if grade[i][j]==0:
            grade[i][j] = 1
            decidido = True
        else:
            i = random.randrange(3)
            j = random.randrange(3)

def TraduzGrade(binaria):
    global grade
    i = 256
    
    for x,linha in enumerate(grade):
        for y,valor in enumerate(linha):
            if binaria>=i:
                grade[x][y] = 2
                binaria -= i
            else:
                grade[x][y] = 0
            i = i//2
    
def GradeBinaria():
    binaria = 0
    i = 1
    for linha in grade:
        for valor in linha:
            if valor!=0:
                binaria += i
            i += i
    return binaria

def InteragirClient():
    global connectionSocket, fim
    
    pergunta = connectionSocket.recv(65000)
    pergunta = int(pergunta)
    print("---------------------------------------")
    print("----------Mensagem Recebida------------")
    print("---------------------------------------")
    if pergunta==0:
        fim = True
        print("Jogo encerrado, finalizando servidor...")
    else:
        TraduzGrade(pergunta)
        print("Cenário Recebido")
        Desenha()
        RespostaAi()
        print("Jogada Enviada")
        Desenha()
        connectionSocket.send(bytes(str(GradeBinaria()), "utf-8"))

def Main():
    global fim
    Desenha()
    
    while not fim:
        InteragirClient()
    
Main()

connectionSocket.close()                            #fecha conexão
print ("////////////////////Servidor Finalizado////////////////////")