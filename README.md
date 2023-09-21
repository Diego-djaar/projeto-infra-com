# projeto-infra-Com

Este projeto foi desenvolvido por alunos de Ciência da Computação do CIn-UFPE para a disciplina de Infraestrutura de Comunicação no semestre 2023.1.

## Integrantes da Equipe

- Ana Sofia de Oliveira Silva Lima (asosl)
- Diego José Arcoverde Agra Rocha (djaar)
- João Vitor Lima Mergulhão (jvlm2)
- João Vítor Cavalcanti Régis (jvcr)
- João Victor Ribeiro Costa de Omena (jvrco)
- Pedro Vítor de Oliveira Monte (pvom)
- Rebeca de Azevedo Menezes (ram3)

## Parte 1

A primeira parte do projeto consiste em fazer uma comunicação cliente-servidor entre dois hosts utilizando o protocolo de transporte UDP. 
Inicialmente, o cliente envia um arquivo (dividido em pacotes de 1KB) ao servidor, que deve salvá-lo e renomeá-lo. Depois disso, o servidor o reenvia ao cliente, que salva a nova cópia com outro nome.

O cliente é o programa client1.py e o servidor é o programa server1.py. Ambos utilizam as funções definidas em file.py.

O nosso "protocolo" da camada de aplicação foi o seguinte: 
- antes do envio do conteúdo de qualquer arquivo, há dois pacotes com informações sobre ele,
- a primeira mensagem enviada deve conter o nome do arquivo,
- a segunda mensagem deve conter o número de pacotes que serão enviados com o conteúdo do arquivo,
- por último, o arquivo é enviado pacote por pacote.

## Parte 2

A segunda parte do projeto se trata de uma implementação do protocolo rdt 3.0 da camada de transporte em uma aplicação de chat multiusuário gerenciado por um servidor e com a utilização do UDP.
