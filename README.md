# projeto-infra-Com

Este projeto foi desenvolvido por alunos de Ciência da Computação do CIn-UFPE para a disciplina de Infraestrutura de Comunicação no semestre 2023.1.

## Integrantes da Equipe

- Ana Sofia de Oliveira Silva Lima (asosl)
- Diego José Arcoverde Agra Rocha (djaar)
- João Vitor Lima Mergulhão (jvlm2)
- João Vítor Cavalcanti Régis (jvcr)
- Rebeca de Azevedo Menezes (ram3)
- João Victor Ribeiro Costa de Omena (jvrco)
- Pedro Vitor de Oliveira Monte (pvom)
## Parte 1

A primeira parte do projeto consiste em fazer uma comunicação cliente-servidor entre dois hosts utilizando o protocolo de transporte UDP. 
Inicialmente, o cliente envia um arquivo (dividido em pacotes de 1KB) ao servidor, que deve salvá-lo e renomeá-lo. Depois disso, o servidor o reenvia ao cliente, que salva a nova cópia com outro nome.

O cliente é o programa client1.py e o servidor é o programa server1.py Ambos utilizam as funções definidas em file.py
