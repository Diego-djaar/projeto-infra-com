from socket import *

class RDT():
    def __init__(self,sock):
        self.sock = sock
    
    def wait_for_ack(ack_num: int, string: str, clientSocket: socket, serverAddr: tuple[str, int], buffer_size: int):
        estado = f"waitack{ack_num}"
        while estado == f"waitack{ack_num}":
            try:
                # Tentar receber a mensagem
                data, clientAdress = clientSocket.recvfrom(buffer_size)
                if (data[0] == ack_num and clientAdress == serverAddr): # Verificação se o ACK corresponde à última msg enviada
                    clientSocket.settimeout(None)
                    ack_num = abs(ack_num - 1) # Troca valor de ACK de 0 pra 1 ou de 1 pra 0
                    estado = f"waitack{ack_num}"
                    return True
                else:
                    continue

            except socket.timeout:
                clientSocket.sendto(string.encode(), serverAddr)
                clientSocket.settimeout(2)
        
    def sendmsg(string: str, seq_num: int, clientSocket: socket, serverAddr: tuple[str, int], buffer_size: int):
        string = str(seq_num) + string # concatenando o sequence number na mensagem
        clientSocket.sendto(string.encode(), serverAddr)
        clientSocket.settimeout(2)