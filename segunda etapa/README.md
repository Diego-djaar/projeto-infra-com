# Parte 1

A primeira parte do projeto consiste em fazer uma comunicação cliente-servidor entre dois hosts utilizando o protocolo de transporte UDP. Inicialmente, o cliente envia um arquivo (dividido em pacotes de 1KB) ao servidor, que deve salvá-lo e renomeá-lo. Depois disso, o servidor o reenvia ao cliente, que salva a nova cópia com outro nome.

O cliente é o programa client1.py e o servidor é o programa server1.py. Ambos utilizam as funções definidas em file.py.

O nosso "protocolo" da camada de aplicação foi o seguinte: 
- antes do envio do conteúdo de qualquer arquivo, há dois pacotes com informações sobre ele,
- a primeira mensagem enviada deve conter o nome do arquivo,
- a segunda mensagem deve conter o número de pacotes que serão enviados com o conteúdo do arquivo,
- por último, o arquivo é enviado pacote por pacote.
