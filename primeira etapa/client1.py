from socket import *
from file import Sendfile, Receivefile
import os
import math
import keyboard

def event(e):
    if e.event_type == keyboard.KEY_DOWN and e.name == 'esc':
        global exit
        print("Conexão encerrada.")
        exit = True
    elif e.event_type == keyboard.KEY_DOWN and e.name == 's': # Se o input for send
        global send
        send = True

# Definições
serverIP = input("Insira o IP do servidor: ")
serverPort = 12000
serverAddr = (serverIP, serverPort) # define tupla com IP e porta de destino
buffer_size = 1024 # define tamnaho do buffer

# Máquina de estados
state = "call0"
exit = False
while (not exit):
    # Esperando input esc do teclado para encerrar a conexão
    keyboard.hook(event)

    if (state == "call0"):
        if (send):
            filePath = input('\nNome do arquivo: ')
            clientSocket = socket(AF_INET, SOCK_DGRAM)  # cria socket para UDP
            print("Enviando...")
            Sendfile(filePath, clientSocket, serverAddr, buffer_size) # envia pacotes
            # Setar timer
            # função para esperar ACK ou timeout e entao decidir o que fazer

    elif (state == "waitACK0"):
        
    elif (state == "call1"):

    elif (state == "waitACK1"):



print("Recebendo...")
Receivefile(clientSocket, buffer_size) # recebe pacotes
