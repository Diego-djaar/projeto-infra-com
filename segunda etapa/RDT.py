from socket import *


class RDT():
    def __init__(self, sock):
        self.sock = sock

    def checksum(data: str):
        chksum = 0
        byte_array = data.encode('utf-8')

        for i in range(0, len(byte_array), 2):
            if i + 1 < len(byte_array):
                byte1 = byte_array[i]
                byte2 = byte_array[i + 1]
                number_16_bits = (byte1 << 8) | byte2
                chksum += number_16_bits
            else:
                chksum += byte_array[i] << 8
        return chksum

    def is_corrupted(self, data: str):
        chksum = self.checksum(data)
        if chksum == data[:3]:
            return False
        return True

    def make_pkt(self, seqnum: int, data: str):
        pkt = str(int) + str(self.checksum(data)) + data #dois primeiros bytes  do pacote correspondem ao checksum
        return pkt

    def wait_for_ack(self, ack_num: int, string: str, clientSocket: socket, serverAddr: tuple[str, int], buffer_size: int):
        estado = f"waitack{ack_num}"
        while estado == f"waitack{ack_num}":
            try:
                # Tentar receber a mensagem
                data, clientAdress = clientSocket.recvfrom(buffer_size)
                # Verificação se o ACK corresponde à última msg enviada
                if (data[0] == ack_num and clientAdress == serverAddr 
                    and self.is_corrupted(data[1:])):
                    clientSocket.settimeout(None)
                    # Troca valor de ACK de 0 pra 1 ou de 1 pra 0
                    ack_num = abs(ack_num - 1)
                    estado = f"waitack{ack_num}"
                    return True
                else:
                    continue

            except socket.timeout:
                clientSocket.sendto(string.encode(), serverAddr)
                clientSocket.settimeout(2)

    def sendmsg(string: str, seq_num: int, clientSocket: socket, serverAddr: tuple[str, int], buffer_size: int):
        # concatenando o sequence number na mensagem
        string = str(seq_num) + string
        clientSocket.sendto(string.encode(), serverAddr)
        clientSocket.settimeout(2)
