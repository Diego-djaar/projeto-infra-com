from socket import *
import os
import math
from RDTs import RDT
import RDTs
import threading


def initserver(serverSocket: socket, serverAddr: tuple[str, int], buffer_size: int, first: bool = True, set_addr: None | str = None) -> RDT:
    print('initializing server')
    objRDT = RDT(serverSocket, set_addr)
    # mesg = objRDT.receivemsg(buffer_size)
    # print(f"RECEIVED CONEXION {mesg[0]}")
    return objRDT


def main():
    # Definições e Inicializar servidor
    serverIP = gethostbyname(gethostname())  # adquirir IP do sevidor
    serverPort = 12000  # define número da porta
    serverSocket = socket(AF_INET, SOCK_DGRAM)  # cria socket UDP para o servidor
    serverSocket.bind(('', serverPort))  # configura o número da porta
    buffer_size = 1024  # define a quantidade de bytes do buffer
    # print('O servidor está pronto para receber')
    # print('O IP do servidor é', serverIP)

    # novo_path, clientAddr = Receivefile(serverSocket, buffer_size)  # recebe pacotes
    # Sendfile(novo_path, serverSocket, clientAddr, buffer_size)  # envia pacotes


if __name__ == "__main__":
    main()
