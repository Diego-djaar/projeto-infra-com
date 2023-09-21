from socket import *
from enum import Enum
import threading
from typing import Any
import traceback
import sys
import importlib
from queue import Queue
from datetime import datetime
# from server1 import connectclient


class RDT_Estados(Enum):
    Chamada_0 = 0
    Ack_0 = 1
    Chamada_1 = 2
    Ack_1 = 3


class RDT_Dest(Enum):
    Baixo_0 = 0
    Baixo_1 = 1


sock: socket
lock_buff = threading.RLock()
lock_sock_recv = threading.RLock()
lock_sock_send = threading.RLock()
lock_list = threading.RLock()
buffsize = 1024
addresslist = []
buff = [Queue()]


def listenloop(type=False, first_con=None):
    # O canal vai ouvir a conexão do socket e retornar 2 casos
    # 1) Criar nova conexão
    # 2) Retornar para a conexão certa
    # Isso irá ouvir o socket e comunicar ao receptor correto do resultado válido

    while True:
        with lock_sock_recv:
            pkt = sock.recvfrom(buffsize)
            pkt = (pkt[0].decode("utf-8"), pkt[1])

        with lock_list:
            # Alternativamente, irá criar uma nova conexão, e então comunicar
            if not pkt[1] in addresslist and not type:  # Se for um endereço novo
                addresslist.append(pkt[1])

                arg = (pkt[1][0], pkt[1][1], pkt[1])
                t = threading.Thread(target=startloop, args=arg, daemon=True)
                t.start()
        with lock_buff:
            # Faz o broadcast
            for b in buff:
                b.put(pkt)


def startloop(serverAddr0, serverAddr1, clientAddr=None):  # LOOP PRINCIPAL DE RECEBER MENSAGENS
    # Isso inicia a thread do RDT, ou seja, a conexão do servidor com um cliente
    # Essa conexão é baseada no ip e na porta

    serverAddr = (serverAddr0, serverAddr1)

    # Chama a função initserver para inicializar o servidor
    mymodule = importlib.import_module('server1')
    initserver = getattr(mymodule, 'initserver')
    if (clientAddr == None):
        conexaoRDT: RDT = initserver(sock, serverAddr, buffsize)
    else:
        conexaoRDT = initserver(sock, serverAddr, buffsize, False, clientAddr)

    # Se conecta ao cliente
    mesg, clientAddr = conexaoRDT.receivemsg(buffsize)
    user_name = mesg[18:]
    print(f"{user_name} entrou na Sala")

    # Loop de receber mensagens
    while True:
        mesg, clientAddr = conexaoRDT.receivemsg(buffsize)
        time = datetime.now()
        time = time.strftime(' %H:%M %d/%m/%Y')
        clientIP, clientPort = clientAddr
        clientPort = str(clientPort)
        mesg = mesg[2:]
        msg = clientIP + ':' + clientPort + '/~' + user_name + ': ' + mesg + ' ' + time
        print(msg)


class RDT():
    buffer: Queue
    buff_index: int
    clientSocket: socket
    estado: RDT_Estados
    estado_dest: RDT_Dest
    retAddress = None
    last_msg: str

    # Isso vai distribuir as mensagens para os RDTs

    def recvfrom(self, is_ack: bool, retAddress0, retAddress1, timeout=9999999) -> tuple[str, Any]:
        # Espera receber uma mensagem correta e então retorna-la para a função correspondente

        if retAddress0 == None:
            retAddress = None
        else:
            retAddress = (retAddress0, retAddress1)
        ack_comp = 1 if is_ack else 0
        while True:
            # Verifica os pacotes do buffer
            pkt = self.buffer.get(timeout=timeout)
            # Verificar se é do tipo e endereço desejado
            if pkt[0][1] == str(ack_comp) and (pkt[1] == retAddress or retAddress == None):
                return pkt

    def __init__(self, clientSocket: socket, retAddr=None):
        sock = clientSocket
        self.estado = RDT_Estados.Chamada_0
        self.estado_dest = RDT_Dest.Baixo_0
        self.retAddress = retAddr
        self.buffer = Queue()
        self.buff_index = buff.__len__()
        buff.append(self.buffer)
        sock.settimeout(None)

    def make_pkt(self, data: str, seqnum: int = 2, is_ack: bool = False) -> str:
        if seqnum == 2:
            seqnum = 0 if self.estado == RDT_Estados.Chamada_0 else 1
        acknum = 1 if is_ack else 0
        pkt = str(seqnum) + str(acknum) + data  # + str(self.checksum(data))
        return pkt

    def wait_for_ack(self, string: str, serverAddr: tuple[str, int], buffer_size: int) -> bool:
        if self.estado == RDT_Estados.Chamada_0 or self.estado == RDT_Estados.Chamada_1:
            raise Exception("ERRO: Esperando ack antes de enviar mensagem")
        while self.estado == RDT_Estados.Ack_0 or self.estado == RDT_Estados.Ack_1:
            try:
                # Tentar receber a mensagem
                data, retAdress = self.recvfrom(True, self.retAddress[0], self.retAddress[1], 2)

                # Verificação se o ACK corresponde à última msg enviada
                ack_num = 0 if self.estado == RDT_Estados.Ack_0 else 1
                if (data[0] == str(ack_num) and retAdress == serverAddr and data[1:] == "1"):

                    # Vai para o próximo estado
                    if self.estado == RDT_Estados.Ack_0:
                        self.estado = RDT_Estados.Chamada_1
                    else:
                        self.estado = RDT_Estados.Chamada_0
                    return True
                else:
                    continue  # Ack incorreto

            except:
                # Timeout da queue
                with lock_sock_send:
                    sock.sendto(string.encode(), serverAddr)
                return False

    def sendmsg(self, string: str, serverAddr: tuple[str, int], buffer_size: int):
        # Envia a mensagem

        if self.estado == RDT_Estados.Ack_0 or self.estado == RDT_Estados.Ack_1:
            raise Exception("ERRO: Enviou mensagem antes de receber ack")

        with lock_sock_send:
            if (self.retAddress == None):
                self.retAddress = serverAddr
            sock.sendto(string.encode(), serverAddr)
            self.last_msg = string

        # Muda para o estado de Ack correspondente
        if self.estado == RDT_Estados.Chamada_0:
            self.estado = RDT_Estados.Ack_0
        else:
            self.estado = RDT_Estados.Ack_1

    def receivemsg(self, buffer_size: int):
        while True:
            # Tentar receber a mensagem
            if self.retAddress == None:
                data, clientAdress = self.recvfrom(False, None, None)
            else:
                data, clientAdress = self.recvfrom(False, self.retAddress[0], self.retAddress[1])

            if (self.retAddress == None):
                self.retAddress = clientAdress
            if (self.retAddress != clientAdress):
                print("TODO clientes diferentes.")

            # Verificação se o sequence number é o próximo esperado
            seq_num = 0 if self.estado_dest == RDT_Dest.Baixo_0 else 1
            if (data[0] == str(seq_num)):  # Se for
                string = self.make_pkt("", seq_num, True)  # Criando pacote ACK
                with lock_sock_send:
                    sock.sendto(string.encode(), clientAdress)

                # Troca de estado
                if self.estado_dest == RDT_Dest.Baixo_0:
                    self.estado_dest = RDT_Dest.Baixo_1
                else:
                    self.estado_dest = RDT_Dest.Baixo_0
                return data, clientAdress
            else:  # Se não for
                string = self.make_pkt("", 0 if seq_num == 1 else 1)  # Reenviar ACK
                with lock_sock_send:
                    sock.sendto(string.encode(), clientAdress)
