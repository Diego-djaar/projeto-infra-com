from socket import *
from enum import Enum
import asyncio
import threading
from typing import Any
import traceback
import sys
import importlib
# from server1 import connectclient


class RDT_Estados(Enum):
    Chamada_0 = 0
    Ack_0 = 1
    Chamada_1 = 2
    Ack_1 = 3


class RDT_Dest(Enum):
    Baixo_0 = 0
    Baixo_1 = 1


class Pkt_buff():
    # Isso serve para guardar as mensagens, e entregar ao RDT correto
    buff: list[tuple[str, Any]]
    addresslist: list
    sock: socket
    buffsize: int
    lock = threading.RLock()
    deleted: int = 0
    import traceback
    import sys

    def startloop(self, serverAddr0, serverAddr1, clientAddr=None):
        print(f"new loop with {serverAddr1}")
        asyncio.run(self.rdtloop(serverAddr0, serverAddr1, clientAddr))

    async def rdtloop(self, serverAddr0, serverAddr1, clientAddr=None):  # LOOP PRINCIPAL DE RECEBER MENSAGENS
        serverAddr = (serverAddr0, serverAddr1)
        mymodule = importlib.import_module('server1')
        connectclient = getattr(mymodule, 'connectclient')
        if (clientAddr == None):
            print(f"looping first")
            conexaoRDT = await connectclient(self, serverAddr, self.buffsize)
        else:
            print(f"looping with {clientAddr}")
            conexaoRDT = await connectclient(self, serverAddr, self.buffsize, False, clientAddr)

        while (True):
            mesg = await conexaoRDT.receivemsg(self.buffsize)
            print(f"RECEIVED CONEXION {mesg[0]}")
            print(f"yay")
            with self.lock:
                print(f"RECEIVED MESSAGE {(await conexaoRDT.receivemsg(self.buffsize))[0]}")
            await asyncio.sleep(0.1)

    def __init__(self, _buffsize: int, _socket: socket):
        self.buffsize = _buffsize
        self.sock = _socket
        self.buff = []
        self.addresslist = []
        pass

    async def bind(self, addr):
        with self.lock:
            print(f'binding {addr}')
            self.sock.bind(addr)

    async def settimeout(self, timeout):
        with self.lock:
            self.sock.settimeout(timeout)

    async def sendto(self, data, addr):
        with self.lock:
            self.sock.sendto(data, addr)

    async def recvfrom(self, is_ack: bool, retAddress0, retAddress1, index: list) -> tuple[str, Any]:
        print(f'hi from {retAddress1}')

        def verify_list():
            if pkt[0][1] == str(ack_comp) and (pkt[1] == retAddress or retAddress == None):  # Verificar se é do tipo e endereço desejado
                print(f"checking {pkt} from {retAddress1}")
                self.deleted += 1
                return self.buff.pop(i)
            elif pkt[1] != retAddress and not retAddress in self.addresslist:  # Se for um endereço novo
                print("Add new RDT")
                self.addresslist.append(retAddress)

                arg = (pkt[1][0], pkt[1][1], pkt[1])
                t = threading.Thread(target=self.startloop, args=arg, daemon=True)
                t.start()

        if retAddress0 == None:
            retAddress = None
        else:
            retAddress = (retAddress0, retAddress1)
        with self.lock:
            # Correr pela lista para encontrar tipo pacote desejado
            # Se encontrar, remover da lista e retornar
            ack_comp = 1 if is_ack else 0
            start = max(index[0] - self.deleted, 0)
            for i in range(start, self.buff.__len__()):
                pkt = self.buff[i]
                verify_list()
            index[0] = self.buff.__len__()

        await asyncio.sleep(0.1)

        while True:
            with self.lock:
                # Receber pacotes da rede ou da lista
                # Se encontrar, retornar
                # Se não, adicionar à lista e dormir
                pkt = self.sock.recvfrom(self.buffsize)
                pkt = (pkt[0].decode("utf-8"), pkt[1])
                print(f"checking {pkt} from {retAddress1}")
                if pkt[0][1] == str(ack_comp) and (pkt[1] == retAddress or retAddress == None):  # Verificar se é do tipo e endereço desejado
                    return pkt
                elif pkt[1] != retAddress and not pkt[1] in self.addresslist:  # Se for um endereço novo
                    print("Add new RDT2")
                    self.addresslist.append(pkt[1])

                    arg = (pkt[1][0], pkt[1][1], pkt[1])
                    self.buff.append(pkt)
                    t = threading.Thread(target=self.startloop, args=arg, daemon=True)
                    t.start()
                else:
                    self.buff.append(pkt)
                    print(f'buff list size is {self.buff.__len__()}')

                # Verificar um da lista
                i = max(index[0] - self.deleted, 0)
                pkt = self.buff[i]
                index[0] += 1  # Avança o ponteiro do RDT, ao verificar cada pacote presente
                if (i < self.buff.__len__()):
                    verify_list()
            print("soninho")
            await asyncio.sleep(0.1)


class RDT():
    lock = threading.Lock()
    clientSocket: Pkt_buff
    estado: RDT_Estados
    estado_dest: RDT_Dest
    retAddress = None
    last_msg: str
    index = [0]

    def __init__(self, clientSocket: Pkt_buff, retAddr=None):
        self.clientSocket = clientSocket
        self.estado = RDT_Estados.Chamada_0
        self.estado_dest = RDT_Dest.Baixo_0
        print(f"started RDT with addr {retAddr}")
        self.retAddress = retAddr

    def make_pkt(self, data: str, seqnum: int = 2, is_ack: bool = False) -> str:
        if seqnum == 2:
            seqnum = 0 if self.estado == RDT_Estados.Chamada_0 else 1
        acknum = 1 if is_ack else 0
        pkt = str(seqnum) + str(acknum) + data  # + str(self.checksum(data))
        return pkt

    async def wait_for_ack(self, string: str, serverAddr: tuple[str, int], buffer_size: int) -> bool:
        if self.estado == RDT_Estados.Chamada_0 or self.estado == RDT_Estados.Chamada_1:
            raise Exception("ERRO: Esperando ack antes de enviar mensagem")
        while self.estado == RDT_Estados.Ack_0 or self.estado == RDT_Estados.Ack_1:
            try:
                # Tentar receber a mensagem
                with self.lock:
                    print(f"Ack from {self.retAddress} {type(self.retAddress)}")
                    data, retAdress = await self.clientSocket.recvfrom(True, self.retAddress[0], self.retAddress[1], self.index)

                # Verificação se o ACK corresponde à última msg enviada
                ack_num = 0 if self.estado == RDT_Estados.Ack_0 else 1
                if (data[0] == str(ack_num) and retAdress == serverAddr and data[1:] == "1"):
                    await self.clientSocket.settimeout(None)

                    # Vai para o próximo estado
                    if self.estado == RDT_Estados.Ack_0:
                        self.estado = RDT_Estados.Chamada_1
                    else:
                        self.estado = RDT_Estados.Chamada_0
                    return True
                else:
                    continue  # Ack incorreto

            except timeout:
                with self.lock:
                    await self.clientSocket.sendto(string.encode(), serverAddr)
                    await self.clientSocket.settimeout(2)
                return False

    async def sendmsg(self, string: str, serverAddr: tuple[str, int], buffer_size: int):
        if self.estado == RDT_Estados.Ack_0 or self.estado == RDT_Estados.Ack_1:
            raise Exception("ERRO: Enviou mensagem antes de receber ack")
        with self.lock:
            if (self.retAddress == None):
                self.retAddress = serverAddr
            await self.clientSocket.sendto(string.encode(), serverAddr)
            self.last_msg = string
            await self.clientSocket.settimeout(2)

        if self.estado == RDT_Estados.Chamada_0:
            self.estado = RDT_Estados.Ack_0
        else:
            self.estado = RDT_Estados.Ack_1

    async def receivemsg(self, buffer_size: int):
        while True:
            # Tentar receber a mensagem
            await self.clientSocket.settimeout(None)
            with self.lock:
                print(f'Receiving from {self.retAddress}')
                if self.retAddress == None:
                    data, clientAdress = await self.clientSocket.recvfrom(False, None, None, self.index)
                else:
                    data, clientAdress = await self.clientSocket.recvfrom(False, self.retAddress[0], self.retAddress[1], self.index)

            print(f"Msg from {clientAdress}")

            if (self.retAddress == None):
                print(f"set dyn RDT with addr {clientAdress}")
                self.retAddress = clientAdress

            if (self.retAddress != clientAdress):
                print("TODO clientes diferentes.")

            # Verificação se o sequence number é o próximo esperado
            seq_num = 0 if self.estado_dest == RDT_Dest.Baixo_0 else 1
            print(f"checking {data}")
            if (data[0] == str(seq_num)):
                string = self.make_pkt("", seq_num, True)  # Criando pacote ACK
                with self.lock:
                    await self.clientSocket.sendto(string.encode(), clientAdress)

                if self.estado_dest == RDT_Dest.Baixo_0:
                    self.estado_dest = RDT_Dest.Baixo_1
                else:
                    self.estado_dest = RDT_Dest.Baixo_0
                return data, clientAdress
            else:
                string = self.make_pkt("", 0 if seq_num == 1 else 1)  # Reenviar ACK
                with self.lock:
                    await self.clientSocket.sendto(string.encode(), clientAdress)
