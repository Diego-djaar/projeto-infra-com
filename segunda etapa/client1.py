from socket import *
from RDT import *
import asyncio
import threading


async def sendRDT(objRDT: RDT, serverAddr: tuple[str, int], buffer_size: int):
    print("Digite a sua mensagem:")
    mensagem = str(input())
    await sendmsg(objRDT, mensagem, 0, serverAddr, buffer_size)


async def connectserver(objRDT: RDT, username: str, serverAddr: tuple[str, int], buffer_size: int):
    msg = f"hi, meu nome eh {username}"
    msg = objRDT.make_pkt(msg)
    await objRDT.sendmsg(msg, serverAddr, buffer_size)
    print("connection sent")
    while not (await objRDT.wait_for_ack(msg, serverAddr, buffer_size)):
        print("waiting ack")
        continue


async def sendmsg(objRDT: RDT, msg: str, serverAddr: tuple[str, int], buffer_size: int):
    msg = objRDT.make_pkt(msg)
    await objRDT.sendmsg(msg, serverAddr, buffer_size)
    print("message sent")
    while not await objRDT.wait_for_ack(msg, serverAddr, buffer_size):
        print("waiting ack")
        continue

async def receiveRDT(RDT: RDT):
    while True:
        msg, clientAdress = RDT.receivemsg()
        if msg[2:5] == "list": # Ajustar para formato padrão da msg dado envio de lista
            is_list = True
        processmsg(msg, is_list)
        
async def processmsg(msg: str, list: bool = False):
    global message_list, user_list
    if not list:
        msg = msg[2:] # A partir de onde for de fato a string (Quando padronizado o formato da mensagem)
        message_list.append(msg)
        print(msg)
    else:
        msg = msg[6:] # A partir de onde tem os nomes dos usuários
        user_list = msg.split("//") # Escolher forma de separação dos usuários da lista a partir de algum padrão
        print("Segue a lista de usuários: ")
        counter = 0
        for i in user_list:
            print(f"({counter}): {i}")
            counter += 1


async def main():
    # Definições
    serverIP = input("Insira o IP do servidor: ")  # Já vai ser conhecido então pode ser implementado sem o input
    serverPort = 12000
    serverAddr = (serverIP, serverPort)  # define tupla com IP e porta de destino
    buffer_size = 1024  # define tamnaho do buffer
    clientSocket = socket(AF_INET, SOCK_DGRAM)  # cria socket para UDP
    sequence_number = "0"

    username = str(input("Qual o seu nome de usuário?"))
    conexaoRDT = RDT(clientSocket)
    await connectserver(conexaoRDT, username, serverAddr, buffer_size)
    print("Você está conectado ao servidor. Caso queira encerrar a conexão digite bye.")
    print("Para ter acesso à lista de usuários digite o comando list.")

    # Iniciar as threads de receber e enviar dados
    receiveThread = threading.Thread(targed = receiveRDT(conexaoRDT), name = "Receive Thread")
    receiveThread.start()

    sendThread = threading.Thread(targed = sendRDT(conexaoRDT, serverAddr, buffer_size), name = "Send Thread")
    sendThread.start()


if __name__ == "__main__":
    asyncio.run(main())
