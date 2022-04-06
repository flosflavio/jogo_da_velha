from socket import *

grade = [[0,0,0],[0,0,0],[0,0,0]]
velha = False
perdeu = False
fim = False
escolhido = 0
atual = 0

serverName = "127.0.0.1"
serverPort = 1200
clientSocket = socket(AF_INET, SOCK_STREAM)

clientSocket.connect((serverName,serverPort))           #conecta

def NovoJogo():
    global grade, velha, perdeu, fim, escolhido

    grade = [[0,0,0],[0,0,0],[0,0,0]]
    velha = False
    perdeu = False
    fim = False
    escolhido = 0
    
def EscolhePeca():
    global escolhido, atual
    
    print ("Escolha sua peça (X ou O)")
    escolhido = input("Sua escolha:")
    TraduzEscolha()
    while escolhido!=1 and escolhido!=2:
        print ("Valor inválido, escolha X ou O")
        escolhido = input("Sua nova escolha:")
        TraduzEscolha()
    
    if escolhido==2:
        print ("Você escolheu X")
    else:
        print ("Você escolheu O")
        
    atual = escolhido
    
def TraduzEscolha():
    global escolhido
    
    if escolhido=="X":
        escolhido = 2
    elif escolhido=="x":
        escolhido = 2
    elif escolhido=="xiz":
        escolhido = 2
    elif escolhido=="Xis":
        escolhido = 2
    elif escolhido=="xis":
        escolhido = 2
    elif escolhido=="XIS":
        escolhido = 2
    elif escolhido=="O":
        escolhido = 1
    elif escolhido=="0":
        escolhido = 1
    elif escolhido=="o":
        escolhido = 1
    else:
        escolhido = 0
    
def ConfereVelha():
    for linha in grade:
        for valor in linha:
            if valor==0:
                return False
    return True

def ConfereLinha(i):
    if grade[i][0]!=0:
        if grade[i][0]==grade[i][1]  and grade[i][0]==grade[i][2]:
            return grade[i][0]
    return 0

def ConfereColuna(i):
    if grade[0][i]!=0:
        if grade[0][i]==grade[1][i]  and grade[0][i]==grade[2][i]:
            return grade[0][i]
    return 0

def ConfereDiagonais():
    if grade[1][1]!=0:
        if (grade[0][0]==grade[1][1]  and grade[2][2]==grade[1][1]) or (grade[0][2]==grade[1][1]  and grade[2][0]==grade[1][1]):
            return grade[1][1]
    return 0

def ConfereTabela():

    resultado = 0
    i=0
    
    if ConfereDiagonais()!=0:
        resultado = ConfereDiagonais()
        
    while i<3 and resultado==0:
        if ConfereColuna(i)!=0:
            resultado = ConfereColuna(i)
        elif ConfereLinha(i)!=0:
            resultado = ConfereLinha(i)
        i += 1

    return resultado

def ConfereResultado():
    global fim, velha, perdeu
    
    if ConfereVelha() or ConfereTabela():
        fim = True

        if ConfereVelha():
            velha = True
        elif ConfereTabela()!=escolhido:
            perdeu = True

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
        
def Pergunta():
    print ("Escolha uma posição")

def SuaJogada():
    print("Seu movimento foi este")
    Desenha()

def JogadaOponente():
    print("O movimento do oponente foi este")
    Desenha()

def Termina():
    if(fim):
        if(velha):
            print ("Deu velha!")
        elif(perdeu):
            print ("Você perdeu!")
        else:
            print ("Você venceu!")

def RespostaJogador():
    global grade
    x = 0
    y = 0
    
    x = input("Escolha uma coluna:")
    while x!="1" and x!="2" and x!="3":
        print ("Resposta inválida")
        x = input("Escolha uma coluna:")
        
    y = input("Escolha uma linha:")
    while y!="1" and y!="2" and y!="3":
        print ("Resposta inválida")
        y = input("Escolha uma linha:")

    x = int(x)-1
    y = int(y)-1

    if grade[y][x]==0:
        grade[y][x] = escolhido
        return True
    else:
        print("Essa posição (", x+1, ", ", y+1, ") está ocupada, escolha outra posição")
        return False

def RespostaServer():
    global clientSocket, grade
    clientSocket.send(bytes(str(GradeBinaria()), "utf-8"))
    
    resposta = clientSocket.recv(1024)
    resposta = int(resposta)
    
    TraduzGrade(resposta)
    
def GradeBinaria():
    binaria = 0
    i = 1
    for linha in grade:
        for valor in linha:
            if valor!=0:
                binaria += i
            i += i
    return binaria

def TraduzGrade(binaria):
    global grade
    i = 256
    
    for x,linha in enumerate(grade):
        for y,valor in enumerate(linha):
            if binaria>=i:
                binaria -= i
                if valor==0:
                    if escolhido==1:
                        grade[x][y] =  2
                    else:
                        grade[x][y] =  1
            i = i//2

def Main():
    global atual
    
    print("+---------------------------------------------+")
    print("|               Jogo da Velha                 |")
    print("+---------------------------------------------+")

    NovoJogo()
    EscolhePeca()
    Desenha()
    
    while not fim:
        if atual==escolhido:
            Pergunta()
            while not RespostaJogador():
                Pergunta()
            SuaJogada()
            atual = escolhido+1
        else:
            RespostaServer()
            JogadaOponente()
            atual = escolhido
        ConfereResultado()
    Termina()
    
Main()
clientSocket.send(bytes("0", "utf-8"))
clientSocket.close()                                    #fecha