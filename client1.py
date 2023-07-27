from socket import *
from file import Sendfile, Receivefile
import os
import math

# Definições
serverIP = input("Insira o IP do servidor: ")
serverPort = 12000
serverAddr = (serverIP, serverPort)
buffer_size = 1024

filePath = input('\nNome do arquivo: ')
clientSocket = socket(AF_INET, SOCK_DGRAM)  # cria socket para UDP

print("Enviando...")
Sendfile(filePath, clientSocket, serverAddr, buffer_size)
print("Recebendo...")
Receivefile(clientSocket, buffer_size)
