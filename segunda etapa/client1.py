from socket import *
from RDTs import *
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
    print("message sent")
    while not objRDT.wait_for_ack(msg, serverAddr, buffer_size):
        print("waiting ack")
        continue


def main():
    # Definições
    serverIP = input("Insira o IP do servidor: ")  # Já vai ser conhecido então pode ser implementado sem o input
    serverPort = 12000
    serverAddr = (serverIP, serverPort)  # define tupla com IP e porta de destino
    buffer_size = 1024  # define tamnaho do buffer
    clientSocket = socket(AF_INET, SOCK_DGRAM)  # cria socket para UDP
    sequence_number = "0"

    username = str(input("Qual o seu nome de usuário?"))
    conexaoRDT = RDT(clientSocket)
    connectserver(conexaoRDT, username, serverAddr, buffer_size)
    print("Você está conectado ao servidor. Caso queira encerrar a conexão digite bye.")
    print("Para ter acesso à lista de usuários digite o comando list.")

    # Iniciar as threads de receber e enviar dados

    async def enviar_mensagens():
        destinatario = str(input("Para qual usuário você deseja enviar?"))
        mensagem = str(input("Digite sua mensagem: "))
        conexaoRDT.sendmsg(mensagem,)


if __name__ == "__main__":
    main()
