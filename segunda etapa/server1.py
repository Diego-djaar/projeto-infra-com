from socket import *
from RDTs import RDT
import RDTs
import threading
import asyncio


def initserver(serverSocket: socket, serverAddr: tuple[str, int], buffer_size: int, first: bool = True, set_addr: None | str = None) -> RDT:
    print('initializing server')
    objRDT = RDT(serverSocket, set_addr)
    # mesg = objRDT.receivemsg(buffer_size)
    # print(f"RECEIVED CONEXION {mesg[0]}")
    return objRDT


async def main():
    serverIP = "127.0.0.1"  # Já vai ser conhecido então pode ser implementado sem o input
    serverPort = 8001
    serverAddr = (serverIP, serverPort)  # define tupla com IP e porta de destino
    buffer_size = 1024  # define tamnaho do buffer
    serverSocket = socket(AF_INET, SOCK_DGRAM)  # cria socket para UDP

    RDTs.sock = serverSocket
    RDTs.sock.bind(serverAddr)

    # Server pov
    t = threading.Thread(target=RDTs.listenloop, daemon=True)
    t.start()

    await asyncio.sleep(999999999999999999999999999999999)


if __name__ == "__main__":
    asyncio.run(main())
