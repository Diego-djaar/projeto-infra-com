from socket import *
from file import Sendfile, Receivefile
import os
import math

# Definições e Inicializar servidor
serverIP = gethostbyname(gethostname()) # adquirir IP do sevidor
serverPort = 12000 # define número da porta
serverSocket = socket(AF_INET, SOCK_DGRAM) # cria socket UDP para o servidor
serverSocket.bind(('', serverPort)) # configura o número da porta
buffer_size = 1024 # define a quantidade de bytes do buffer
print('O servidor está pronto para receber')
print('O IP do servidor é', serverIP)

novo_path, clientAddr = Receivefile(serverSocket, buffer_size) # recebe pacotes
Sendfile(novo_path, serverSocket, clientAddr, buffer_size) # envia pacotes
