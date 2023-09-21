from socket import *
from RDTs import *
import RDTs
import threading


def sendRDT(objRDT: RDT, serverAddr: tuple[str, int], buffer_size: int):
    print("Digite a sua mensagem:")
    mensagem = str(input())
    objRDT.sendmsg(f"{mensagem}", 0, serverAddr, buffer_size)


def connectserver(objRDT: RDT, username: str, serverAddr: tuple[str, int], buffer_size: int):
    msg = f"hi, meu nome eh {username}"
    msg = objRDT.make_pkt(msg)
    objRDT.sendmsg(msg, serverAddr, buffer_size)
    print("conexion sent")
    while not (objRDT.wait_for_ack(msg, serverAddr, buffer_size)):
        print("waiting ack")
        continue


def sendmsg(objRDT: RDT, msg: str, serverAddr: tuple[str, int], buffer_size: int):
    msg = objRDT.make_pkt(msg)
    objRDT.sendmsg(msg, serverAddr, buffer_size)
    while not objRDT.wait_for_ack(msg, serverAddr, buffer_size):
        continue


def main():
    # Definições
    serverIP = "127.0.0.1"  # Já vai ser conhecido então pode ser implementado sem o input
    serverPort = 8001
    clientPort = 8002
    serverAddr = (serverIP, serverPort)  # define tupla com IP e porta de destino
    clientAddr = (serverIP, clientPort)  # define tupla com IP e porta de destino
    buffer_size = 1024  # define tamnaho do buffer
    clientSocket = socket(AF_INET, SOCK_DGRAM)  # cria socket para UDP
    serverSocket = socket(AF_INET, SOCK_DGRAM)  # cria socket para UDP

    username = str(input("hi, meu nome eh "))

    RDTs.sock = clientSocket
    RDTs.is_server = False
    t = threading.Thread(target=listenloop, args=(True, clientSocket), daemon=True)
    t.start()

    conexaoRDT = RDT(clientSocket)
    connectserver(conexaoRDT, username, serverAddr, buffer_size)
    print("Você está conectado ao servidor. Caso queira encerrar a conexão digite bye.")
    print("Para ter acesso à lista de usuários digite o comando list.")

    def chat_pub():
        while True:
            mesg, serverAddr = conexaoRDT.receivemsg(buffsize)
            print(mesg[2:])

    t = threading.Thread(target=chat_pub, daemon=True)
    t.start()

    while True:
        msg = input()
        if msg == "list":
            sendmsg(conexaoRDT, "list", serverAddr, buffer_size)
        elif msg == "bye":
            exit(0)
        else:
            sendmsg(conexaoRDT, msg, serverAddr, buffer_size)


if __name__ == "__main__":
    main()
