from socket import *
from file import Sendfile, Receivefile
import os
import math
import keyboard
import time
import threading

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
clientSocket = socket(AF_INET, SOCK_DGRAM)  # cria socket para UDP
sequence_number = "0"

# Máquina de estados
state = "call0"
exit = False
print("Aperte a tecla s para enviar um arquivo ou esc para sair")
while (not exit):
    # Esperando input do teclado para encerrar a conexão
    keyboard.hook(event)

    if (state == "call0"):
        if (send):
            filePath = input('\nNome do arquivo: ')
            print("Enviando...")
            Sendfile(filePath, clientSocket, serverAddr, buffer_size) # envia pacotes
            state = "waitACK0"

    elif (state == "waitACK0"):
        print("Recebendo...")
        Receivefile(clientSocket, buffer_size, sequence_number) # recebe pacotes
        if sequence_number == "1":
            print("Reenviando...")
            Sendfile(filePath, clientSocket, serverAddr, buffer_size) # envia pacotes
        # Falta lidar com timeout e testar
    elif (state == "call1"):

    elif (state == "waitACK1"):



# print("Recebendo...")
# Receivefile(clientSocket, buffer_size) # recebe pacotes
