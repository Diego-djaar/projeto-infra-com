from socket import *
import os
import math
from time import sleep

# envia arquivo
def Sendfile(filePath: str, clientSocket: socket, serverAddr: tuple[str, int], buffer_size: int, seq_num: str):
    with open(filePath, 'rb') as file: # arquivo binário em modo de leitura
        # Enviando nome do arquivo
        filePath_list = filePath.split('\\') # o caminho do arquivo é separado em uma lista usando como delimitador '\' -> pensadno em windows
        arquivo_nome = filePath_list[-1] # extrai o nome do arquivo pegando o último elemento da lista
        clientSocket.sendto(arquivo_nome.encode(), serverAddr) # envia o nome codificado para serverAddr (tupla que especifica o IP e a porta de destino)

        # Enviando numero de pacotes do arquivo
        n_pacotes = math.ceil(os.path.getsize(filePath)/buffer_size)
        clientSocket.sendto(str(n_pacotes).encode(), serverAddr)

        data = file.read(buffer_size)

        clientSocket.sendto(seq_num.encode(), serverAddr) # Enviando sequence number

        # Enviando conteúdo do arquivo pacote a pacote (cada um tem buffer_size bytes)
        for i in range(0, n_pacotes):
            if (clientSocket.sendto(data, serverAddr)): # envia data e checa se foi bem sucedido
                sleep(0.02) # delay entre envio de pacotes
                data = file.read(buffer_size) # atualiza variável data

# recebe, salva e renomeia arquivo
def Receivefile(serverSocket: socket, buffer_size: int) -> tuple[str, any]:
    # Receber nome
    data, clientAddr = serverSocket.recvfrom(buffer_size)
    name, type = data.decode().split('.') # extrai o nome e o tipo de arquivo
    filePath = name + '_enviado.' + type # muda o nome do arquivo

    # Recebe número de pacotes 
    data, clientAddr = serverSocket.recvfrom(buffer_size) # clientAddr é tupla que especifica o IP e a porta de destino do host que está enviando
    n_pacotes = int(data.decode()) # decodifica a mensagem

    seq_number = serverSocket.recvfrom(buffer_size).decode()

    # cria novo arquivo e escreve o conteúdo
    with open(filePath, 'wb') as file: # arquivo binário em modo de escrita
        print(filePath)
        try:
            for i in range(0, n_pacotes):
                data, clientAddr = serverSocket.recvfrom(buffer_size) # recebe os pacotes por meio do socket serverSocket
                file.write(data)
                serverSocket.settimeout(2) # seta tempo para timout como 2 segundos
        except timeout: # caso ocorra um timeout o arquivo e o socket são fechados
            file.close()
            serverSocket.close()
            print('Timeout')

    return (filePath, clientAddr, seq_number)
