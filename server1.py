from socket import *
serverPort = 12000 # porta em que vamos receber as mensagens
serverSocket = socket(AF_INET,SOCK_DGRAM) # cria socket UDP
serverSocket.bind(('', serverPort)) 
buffer_size = 1024
file = open('logo_rcv.png','wb')
print('The server is ready to receive')

while 1:
    data,clientAddr = serverSocket.recvfrom(buffer_size)
    try:
        while(data):
            file.write(data)
            serverSocket.settimeout(2)
            data,clientAddr = serverSocket.recvfrom(buffer_size)
    except timeout:
        file.close()
        serverSocket.close()
        print ('File Downloaded')
