from socket import *
serverName = "192.168.0.148" # ip do sevidor
serverPort = 12000 # porta para a qual as mensagens são enviadas no servidor
buffer_size = 1024 # 1024 bytes de buffer -> tamanho do pacote
file = open('logo.png', 'rb') 
clientSocket = socket(AF_INET, SOCK_DGRAM) # cria socket para UDP

data = file.read(buffer_size)

while (data):
    if(clientSocket.sendto(data,(serverName, serverPort))):
        print("sending ...")
        data = file.read(buffer_size)
