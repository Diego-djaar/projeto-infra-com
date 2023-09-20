from socket import *
from RDT import *
import asyncio
import threading


async def sendRDT(objRDT: RDT, serverAddr: tuple[str, int], buffer_size: int):
    print("Digite a sua mensagem:")
    mensagem = str(input())
    await sendmsg(objRDT, mensagem, serverAddr, buffer_size)


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

async def receiveRDT(RDT: RDT, buffer_size: int):
    while True:
        msg = RDT.receivemsg(buffer_size)[0]
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
    serverIP = "127.0.0.1"  # Já vai ser conhecido então pode ser implementado sem o input
    serverPort = 8001
    clientPort = 8002
    serverAddr = (serverIP, serverPort)  # define tupla com IP e porta de destino
    clientAddr = (serverIP, clientPort)  # define tupla com IP e porta de destino
    buffer_size = 1024  # define tamnaho do buffer
    clientSocket = socket(AF_INET, SOCK_DGRAM)  # cria socket para UDP
    serverSocket = socket(AF_INET, SOCK_DGRAM)  # cria socket para UDP

    username = str(input("Qual o seu nome de usuário?"))
    pktBuff = Pkt_buff(buffer_size, serverSocket)
    conexaoRDT = RDT(pktBuff)
    await connectserver(conexaoRDT, username, serverAddr, buffer_size)
    print("Você está conectado ao servidor. Caso queira encerrar a conexão digite bye.")
    print("Para ter acesso à lista de usuários digite o comando list.")

    # Iniciar as threads de receber e enviar dados
    # receiveThread = threading.Thread(target =, args =)
    # receiveThread.start()


    #sendThread = threading.Thread(target = await sendRDT(conexaoRDT, serverAddr, buffer_size), name = "Send Thread")
    #sendThread.start()


if __name__ == "__main__":
    asyncio.run(main())
