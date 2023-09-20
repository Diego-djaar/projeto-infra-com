from socket import *
from RDT import *
import threading

def sendRDT(objRDT: RDT, serverAddr: tuple[str, int], buffer_size: int):
    global sequence_number, username
    print("Digite a sua mensagem:")
    mensagem = str(input())
    objRDT.sendmsg(f"{mensagem}", 0, serverAddr, buffer_size)
    

def connectserver(objRDT: RDT, username: str, serverAddr: tuple[str, int], buffer_size: int):
    global sequence_number
    objRDT.sendmsg(f"hi, meu nome eh {username}", 0, serverAddr, buffer_size)
    sequence_number = "1"

def receiveRDT(RDT: RDT):
    while True:
        msg, clientAdress = RDT.receivemsg()
        if msg[1:4] == "list": # Ajustar para formato padrão da msg dado envio de lista
            is_list = True
        processmsg(msg, is_list)
        
def processmsg(msg: str, list: bool = False):
    global message_list
    if not list:
        msg = msg[4:] # A partir de onde for de fato a string (Quando padronizado o formato da mensagem)
        message_list.append(msg)
        print(msg)

        

# Definições
serverIP = input("Insira o IP do servidor: ") # Já vai ser conhecido então pode ser implementado sem o input
serverPort = 12000
serverAddr = (serverIP, serverPort) # define tupla com IP e porta de destino
buffer_size = 1024 # define tamnaho do buffer
clientSocket = socket(AF_INET, SOCK_DGRAM)  # cria socket para UDP
sequence_number = "0"
message_list = []

username = str(input("Qual o seu nome de usuário?"))
conexaoRDT = RDT(clientSocket)
connectserver(conexaoRDT, username, serverAddr, buffer_size)
print("Você está conectado ao servidor. Caso queira encerrar a conexão digite bye.")
print("Para ter acesso à lista de usuários digite o comando list.")

# Iniciar as threads
receiveThread = threading.Thread(targed = receiveRDT, name = "Receive Thread")
receiveThread.start()