from socket import *
import os
import math
from time import sleep


def Sendfile(filePath: str, clientSocket: socket, serverAddr: tuple[str, int], buffer_size: int):
    with open(filePath, 'rb') as file:
        # Enviando nome do arquivo
        filePath_list = filePath.split('\\')
        arquivo_nome = filePath_list[-1]
        clientSocket.sendto(arquivo_nome.encode(), serverAddr)

        # Enviando numero de pacotes do arquivo
        n_pacotes = math.ceil(os.path.getsize(filePath)/buffer_size)
        clientSocket.sendto(str(n_pacotes).encode(), serverAddr)

        data = file.read(buffer_size)

        for i in range(0, n_pacotes):
            if (clientSocket.sendto(data, serverAddr)):
                sleep(0.02)
                data = file.read(buffer_size)


def Receivefile(serverSocket: socket, buffer_size: int) -> tuple[str, any]:
    # Receber nome
    data, clientAddr = serverSocket.recvfrom(buffer_size)
    name, type = data.decode().split('.')
    filePath = name + '_enviado.' + type

    # Receber tamanho
    data, clientAddr = serverSocket.recvfrom(buffer_size)
    n_pacotes = int(data.decode())

    with open(filePath, 'wb') as file:
        print(filePath)
        try:
            for i in range(0, n_pacotes):
                data, clientAddr = serverSocket.recvfrom(buffer_size)
                file.write(data)
                serverSocket.settimeout(2)
        except timeout:
            file.close()
            serverSocket.close()
            print('Timeout')

    return (filePath, clientAddr)
