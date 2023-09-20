from socket import *
from enum import Enum
import asyncio
import threading
from typing import Any


class RDT_Estados(Enum):
    Chamada_0 = 0
    Ack_0 = 1
    Chamada_1 = 2
    Ack_1 = 3


class RDT_Dest(Enum):
    Baixo_0 = 0
    Baixo_1 = 1

# Isso serve para guardar as mensagens, e entregar ao RDT correto


class Pkt_buff():
    buff: list[tuple[str, Any]]
    sock: socket
    buffsize: int
    lock = threading.Lock()
    deleted: int = 0

    def __init__(self, _buffsize: int, _socket: socket):
        self.buffsize = _buffsize
        self.sock = _socket
        self.buff = []
        pass

    async def bind(self, addr):
        with self.lock:
            self.sock.bind(addr)

    async def settimeout(self, timeout):
        with self.lock:
            self.sock.settimeout(timeout)

    async def sendto(self, data, addr):
        with self.lock:
            self.sock.sendto(data, addr)

    async def recvfrom(self, is_ack: bool, retAddress0, retAddress1) -> tuple[str, Any]:
        if retAddress0 == None:
            retAddress = None
        else:
            retAddress = (retAddress0, retAddress1)
        with self.lock:
            # Correr pela lista para encontrar tipo pacote desejado
            # Se encontrar, remover da lista e retornar
            ack_comp = 1 if is_ack else 0
            for i in range(0, self.buff.__len__()):
                pkt = self.buff[i]
                if pkt[0][1] == str(ack_comp) and (pkt[1] == retAddress or retAddress == None):  # Verificar se é do tipo e endereço desejado
                    self.deleted += 1
                    return self.buff.pop(i)
        while True:
            with self.lock:
                # Receber pacotes da rede
                # Se encontrar, retornar
                # Se não, adicionar à lista e dormir
                pkt = self.sock.recvfrom(self.buffsize)
                pkt = (pkt[0].decode("utf-8"), pkt[1])
                if pkt[0][1] == str(ack_comp) and (pkt[1] == retAddress or retAddress == None):  # Verificar se é do tipo e endereço desejado
                    return pkt
                else:
                    self.buff.append(pkt)
            await asyncio.sleep(0.5)


class RDT():
    lock = threading.Lock()
    clientSocket: Pkt_buff
    estado: RDT_Estados
    estado_dest: RDT_Dest
    retAddress = None
    last_msg: str

    def __init__(self, clientSocket: Pkt_buff, retAddr=None):
        self.clientSocket = clientSocket
        self.estado = RDT_Estados.Chamada_0
        self.estado_dest = RDT_Dest.Baixo_0
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
                    data, retAdress = await self.clientSocket.recvfrom(True, self.retAddress[0], self.retAddress[1])

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
                if self.retAddress == None:
                    data, clientAdress = await self.clientSocket.recvfrom(False, None, None)
                else:
                    data, clientAdress = await self.clientSocket.recvfrom(False, self.retAddress[0], self.retAddress[1])

            print(f"Msg from {clientAdress}")

            if (self.retAddress == None):
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
