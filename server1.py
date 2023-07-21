from socket import *

serverIP = gethostbyname(gethostname())

serverPort = 12000  # porta em que vamos receber as mensagens
serverSocket = socket(AF_INET, SOCK_DGRAM)  # cria socket UDP
serverSocket.bind(('', serverPort))
buffer_size = 1024

print('The server is ready to receive')
print('The server IP is ', serverIP)

data, clientAddr = serverSocket.recvfrom(buffer_size)

name, type = data.decode().split('.')
fileName = name + '_there.' + type
file = open(fileName, 'wb')

print(fileName)

while 1:
    try:
        data, clientAddr = serverSocket.recvfrom(buffer_size)
        while (data):
            file.write(data)
            serverSocket.settimeout(2)
            data, clientAddr = serverSocket.recvfrom(buffer_size)
    except timeout:
        file.close()
        serverSocket.close()
        print('File Downloaded')
        break
