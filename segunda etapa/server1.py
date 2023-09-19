from socket import *
from file import Sendfile, Receivefile
from datetime import datetime

# Definições e Inicializar servidor
serverIP = gethostbyname(gethostname()) # adquirir IP do sevidor
serverPort = 12000 # define número da porta
serverSocket = socket(AF_INET, SOCK_DGRAM) # cria socket UDP para o servidor
serverSocket.bind(('', serverPort)) # configura o número da porta
buffer_size = 1024 # define a quantidade de bytes do buffer
print('O servidor está pronto para receber')
print('O IP do servidor é', serverIP)

users_dict = {}
users_list = []

while True:
    pkt_rcv = serverSocket.recvfrom(buffer_size) # recebe pacotes
    if pkt_rcv:
        data, clientAddr = pkt_rcv
        data = data.decode() #decodifica mensagem
        if data[:16] == "hi, meu nome eh":
            if not (clientAddr in users_dict):
                user_name = data[17:]
                users_list.append(user_name)
                users_dict[clientAddr] = user_name
                msg = user_name +' adicionado'
                print(msg)
                broadcast = True
        else:
            user_name = users_dict.pop(clientAddr, False)
            if user_name:
                if data[:4] == "bye":
                    user_name = users_dict.pop(clientAddr, False)
                    users_list.remove(user_name)
                    if user_name:
                        msg = user_name +' saiu do chat'
                        print(msg)
                        broadcast = True
                elif data[:4] == "list":
                    serverSocket.sendto(str(users_list).encode(), clientAddr) # envia pacotes
                    broadcast = False
                else:
                    time = datetime.now()
                    time = time.strftime(' %H:%M %d/%m/%Y')
                    clientIP, clientPort = clientAddr
                    clientPort = str(clientPort)
                    msg = clientIP + ':' + clientPort + '~' + user_name + msg + time

        if broadcast:
            for clientAddr,user_name in users_dict.items(): #broadcast
                serverSocket.sendto(msg.encode(), clientAddr) # envia pacotes


        

   

