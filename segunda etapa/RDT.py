from socket import *


class RDT():
    def __init__(self, clientSocket):
        self.clientSocket = clientSocket

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
            chksum = ~chksum
        return chksum

    def is_corrupted(self, data: str):
        chksum = self.checksum(data)
        if chksum == data[:3]:
            return False
        return True

    def make_pkt(self, seqnum: int, data: str):
        pkt = str(seqnum) + str(self.checksum(data)) + data # dois primeiros bytes  do pacote correspondem ao checksum
        return pkt

    def wait_for_ack(self, ack_num: int, string: str, serverAddr: tuple[str, int], buffer_size: int):
        estado = f"waitack{ack_num}"
        while estado == f"waitack{ack_num}":
            try:
                # Tentar receber a mensagem
                data, clientAdress = self.clientSocket.recvfrom(buffer_size)
                # Verificação se o ACK corresponde à última msg enviada
                if (data[0] == ack_num and clientAdress == serverAddr 
                    and not self.is_corrupted(data[1:])):
                    self.clientSocket.settimeout(None)
                    # Troca valor de ACK de 0 pra 1 ou de 1 pra 0
                    ack_num = abs(ack_num - 1)
                    estado = f"waitack{ack_num}"
                    return True
                else:
                    continue

            except socket.timeout:
                self.clientSocket.sendto(string.encode(), serverAddr)
                self.clientSocket.settimeout(2)

    def sendmsg(self, string: str, seq_num: int, serverAddr: tuple[str, int], buffer_size: int):
        string = self.make_pkt(seq_num, string)
        self.clientSocket.sendto(string.encode(), serverAddr)
        self.clientSocket.settimeout(2)

    def receivemsg(self, seq_num: int, buffer_size: int):
        estado = f"waitseq{seq_num}"
        while (estado == f"waitseq{seq_num}"):
            # Tentar receber a mensagem
            data, clientAdress = self.clientSocket.recvfrom(buffer_size)
            # Verificação se o sequence number é o próximo esperado
            if (data[0] == seq_num and not self.is_corrupted(data[1:])):
                string = self.make_pkt(seq_num, "ACK") # Criando pacote ACK
                self.clientSocket.sendto(string.encode(), clientAdress)
                seq_num = abs(seq_num - 1)
                estado = f"waitseq{seq_num}"
            
            return data, clientAdress