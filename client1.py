from socket import *
serverIP = input("insert server IP: ")  # ip do sevidor
serverPort = 12000  # porta para a qual as mensagens são enviadas no servidor
buffer_size = 1024  # 1024 bytes de buffer -> tamanho do pacote

filePath = input('\nPath of the file you want to send: ')
file = open(filePath, 'rb')
clientSocket = socket(AF_INET, SOCK_DGRAM)  # cria socket para UDP

filePath_list = filePath.split('\\')  
clientSocket.sendto(filePath_list[-1].encode(), (serverIP, serverPort)) # enviando nome do arquivo

data = file.read(buffer_size)

while (data):
    if (clientSocket.sendto(data, (serverIP, serverPort))):
        print("sending ...")
        data = file.read(buffer_size)
