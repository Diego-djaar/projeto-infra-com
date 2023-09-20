from socket import *
from RDT import *
import threading

# Definições
# Já vai ser conhecido então pode ser implementado sem o input
serverIP = input("Insira o IP do servidor: ")
serverPort = 12000
serverAddr = (serverIP, serverPort)  # define tupla com IP e porta de destino
buffer_size = 1024  # define tamnaho do buffer
clientSocket = socket(AF_INET, SOCK_DGRAM)  # cria socket para UDP
sequence_number = "0"

print("Você está conectado ao servidor. Caso queira encerrar a conexão digite bye.")
print("Para ter acesso à lista de usuários digite o comando list.")


while True:
    msg = input('Você: ')
    if msg == 'EXIT':
        break
    if msg == 'bye':
        print('Você saiu do chat')

    clientSocket.sendto(msg.encode(), serverAddr)

    try:
        data_rcv, addr = clientSocket.recvfrom(buffer_size)  # recebe pacotes
        clientSocket.settimeout(1)
    except:
        continue
    finally:
        if data_rcv:
            print(data_rcv.decode())
            data_rcv = False

# Iniciar as threads de receber e enviar dados
