from socket import *
from enum import Enum
import asyncio
import threading


class RDT_Estados(Enum):
    Chamada_0 = 0
    Ack_0 = 1
    Chamada_1 = 2
    Ack_1 = 3


class RDT_Dest(Enum):
    Baixo_0 = 0
    Baixo_1 = 1


class RDT():
    lock = threading.Lock()
    clientSocket: socket
    estado: RDT_Estados
    estado_dest: RDT_Dest
    last_msg: str

    def __init__(self, clientSocket):
        self.clientSocket = clientSocket
        self.estado = RDT_Estados.Chamada_0
        self.estado_dest = RDT_Dest.Baixo_0

    def make_pkt(self, data: str, seqnum: int = 2) -> str:
        if seqnum == 2:
            seqnum = 0 if self.estado == RDT_Estados.Chamada_0 else 1
        pkt = str(seqnum) + data  # + str(self.checksum(data))
        return pkt

    async def wait_for_ack(self, string: str, serverAddr: tuple[str, int], buffer_size: int) -> bool:
        if self.estado == RDT_Estados.Chamada_0 or self.estado == RDT_Estados.Chamada_1:
            raise Exception("ERRO: Esperando ack antes de enviar mensagem")
        while self.estado == RDT_Estados.Ack_0 or self.estado == RDT_Estados.Ack_1:
            try:
                # Tentar receber a mensagem
                with self.lock:
                    (data, clientAdress) = self.clientSocket.recvfrom(4)

                data = data.decode("utf-8")
                # Verificação se o ACK corresponde à última msg enviada
                ack_num = 0 if self.estado == RDT_Estados.Ack_0 else 1
                if (data[0] == str(ack_num) and clientAdress == serverAddr and data[1:] == "ACK"):
                    self.clientSocket.settimeout(None)

                    # Vai para o próximo estado
                    if self.estado == RDT_Estados.Ack_0:
                        self.estado = RDT_Estados.Chamada_1
                    else:
                        self.estado = RDT_Estados.Chamada_0
                    return True
                else:
                    continue

            except timeout:
                with self.lock:
                    self.clientSocket.sendto(string.encode(), serverAddr)
                    self.clientSocket.settimeout(2)
                return False

    async def sendmsg(self, string: str, serverAddr: tuple[str, int], buffer_size: int):
        if self.estado == RDT_Estados.Ack_0 or self.estado == RDT_Estados.Ack_1:
            raise Exception("ERRO: Enviou mensagem antes de receber ack")
        # string = self.make_pkt(0 if self.estado == RDT_Estados.Chamada_0 else 1, string)
        with self.lock:
            self.clientSocket.sendto(string.encode(), serverAddr)
            self.last_msg = string
            self.clientSocket.settimeout(2)

        if self.estado == RDT_Estados.Chamada_0:
            self.estado = RDT_Estados.Ack_0
        else:
            self.estado = RDT_Estados.Ack_1

    async def receivemsg(self, buffer_size: int):
        while True:
            # Tentar receber a mensagem
            try:
                with self.lock:
                    data, clientAdress = self.clientSocket.recvfrom(buffer_size)
                # Verificação se o sequence number é o próximo esperado
                seq_num = 0 if self.estado_dest == RDT_Dest.Baixo_0 else 1
                data = data.decode("utf-8")
                print(f"checking {data}")
                print(data[0])
                print(str(seq_num))
                if (data[0] == str(seq_num)):
                    string = self.make_pkt("ACK", seq_num)  # Criando pacote ACK
                    with self.lock:
                        self.clientSocket.sendto(string.encode(), clientAdress)

                    if self.estado_dest == RDT_Dest.Baixo_0:
                        self.estado_dest = RDT_Dest.Baixo_1
                    else:
                        self.estado_dest = RDT_Dest.Baixo_0
                    return data, clientAdress

            except timeout:
                continue
