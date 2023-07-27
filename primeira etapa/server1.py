from socket import *
from file import Sendfile, Receivefile
import os
import math

# Definições e Inicializar servidor
serverIP = gethostbyname(gethostname())
serverPort = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))
buffer_size = 1024
print('O servidor está pronto para receber')
print('O IP do servidor é', serverIP)

novo_path, clientAddr = Receivefile(serverSocket, buffer_size)
Sendfile(novo_path, serverSocket, clientAddr, buffer_size)
