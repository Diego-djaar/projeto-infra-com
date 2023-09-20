from socket import *
from enum import Enum
from file import Sendfile, Receivefile
import asyncio
import threading
from RDT import *
from client1 import *
from server1 import *


async def main():
    # Definições
    serverIP = "127.0.0.1"  # Já vai ser conhecido então pode ser implementado sem o input
    serverPort = 8001
    clientPort = 8002
    serverAddr = (serverIP, serverPort)  # define tupla com IP e porta de destino
    clientAddr = (serverIP, clientPort)  # define tupla com IP e porta de destino
    buffer_size = 1024  # define tamnaho do buffer
    clientSocket = socket(AF_INET, SOCK_DGRAM)  # cria socket para UDP
    serverSocket = socket(AF_INET, SOCK_DGRAM)  # cria socket para UDP

    # Cliente pov
    username = "Dhayego"
    conexaoRDT = RDT(clientSocket)
    await connectserver(conexaoRDT, username, serverAddr, buffer_size)
    await sendmsg(conexaoRDT, "Lá e de volta", serverAddr, buffer_size)
    await sendmsg(conexaoRDT, "Outra vez", serverAddr, buffer_size)


if __name__ == "__main__":
    asyncio.run(main())
