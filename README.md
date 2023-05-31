# Reconhecimento de dígitos do painel de senha do restaurante do Insper

## Descrição do projeto e problema a ser estudado

O objetivo deste projeto é desenvolver uma solução para permitir que os clientes do restaurante do 6° andar do prédio 2 da faculdade Insper possam acompanhar a senha atual sem precisar estar próximo do painel. Notamos no nosso dia a dia que muitos alunos não conseguem ouvir ou ver a senha atual, já que a maior parte dos assentos fica longe do painel.

## Origem dos dados

Os dados para o teste das técnicas de OCR foram gerados por meio de um vídeo e de fotos feitas por nós do painel de senha do restaurante do Insper. Utilizamos essas imagens para construir a máscara e definir os ajustes de imagem que permitem o reconhecimento de dígitos.

## Técnicas para extrair e tratar os dados

Fizemos o tratamento das imagens por meio de técnicas de OpenCV e OCR para extrair os dígitos do painel.  Utilizaremos a biblioteca EasyOCR para realizar o OCR.

## Ideia de solução
Uma solução proposta para o projeto envolve a utilização de um Raspberry Pi com uma câmera posicionada de forma a capturar o painel de senhas do restaurante do Insper. O Raspberry Pi ficaria responsável por tirar fotos periódicas do painel e enviar essas imagens para a API de Reconhecimento de Dígitos.

A API recebe as fotos enviadas pelo Raspberry Pi por meio da rota /upload, realizaria o processo de reconhecimento óptico de caracteres (OCR) para extrair o número da senha atual e armazenaria esse número em um banco de dados.

Para permitir que os clientes do restaurante acompanhem a senha sendo chamada, um frontend foi desenvolvido. Esse frontend utiliza a rota / da API para obter o número da senha atual do banco de dados e exibiria essa informação de forma clara e visível para os clientes.

Dessa forma, os clientes poderiam visualizar o número da senha atual em tempo real por meio do frontend, sem a necessidade de se aproximarem fisicamente do painel de senhas. Isso proporcionaria maior comodidade e conveniência para os usuários, melhorando a experiência de atendimento no restaurante do Insper.

# Descrição dos Arquivos do Projeto

1. `teste.py` - Este arquivo foi criado como prova de conceito para testar a máscara e o OCR com fotos tiradas previamente, armazenadas na pasta `data/img`. Ele realiza um tratamento nas imagens para melhorar a eficácia do OCR. Primeiro, é aplicada uma máscara para destacar os dígitos, que são quase totalmente brancos, já que o painel de senha é iluminado. Em seguida, é utilizado o `bitwise_not` para inverter as cores da imagem, deixando os dígitos pretos e o fundo branco. Uma transformação morfológica é aplicada para realçar ainda mais os dígitos. Por fim, o OCR é utilizado (no caso, o EasyOCR) para reconhecer os dígitos presentes na imagem tratada. O resultado final é uma lista de dígitos reconhecidos.

2. `tira_foto.py` - Este arquivo é responsável pelo código executado no Raspberry Pi. Ele tira fotos do painel de senha a cada segundo e salva as imagens na pasta `pictures`. O código permite que apenas uma foto esteja presente na pasta, para evitar que o espaço seja ocupado por múltiplas imagens. A foto é salva com o nome "image.jpg" e é substituída a cada nova captura. Em seguida, a imagem é enviada para uma API por meio da rota "/upload", onde é realizado um tratamento semelhante ao `teste.py`. A imagem é processada

Imagem original do painel de senha |  Imagem tratada
:-------------------------:|:-------------------------:
![](readme_files/original_img.jpg)  |  ![](readme_files/mask.jpg)

# API de Reconhecimento de Dígitos do Painel de Senha do Restaurante do Insper

Esta API foi desenvolvida como parte de um projeto para permitir que os clientes do restaurante do 6° andar do prédio 2 da faculdade Insper possam acompanhar a senha atual sem precisar estar próximo do painel. O objetivo é utilizar técnicas de reconhecimento de dígitos por meio de imagens para extrair as informações do painel de senha, armazená-las em um banco de dados e disponibilizá-las para os clientes. Para a API foi utilizado o framework FastAPI.

## Descrição dos Arquivos

A API é composta pelos seguintes arquivos:

### config.py

O arquivo `config.py` contém as configurações da aplicação. Ele define as configurações de ambiente e a classe `Settings` que armazena as configurações obtidas do ambiente. A função `get_settings()` retorna uma instância da classe `Settings` com as configurações.

### healthcheck.py

O arquivo `healthcheck.py` contém a definição da rota `/health` da API. Essa rota retorna um JSON com informações sobre a saúde da aplicação, incluindo o status "healthy", o ambiente em que a API está sendo executada e se o modo de teste está ativado ou não.

### main.py

O arquivo `main.py` é o ponto de entrada principal da aplicação da API. Ele cria a instância do aplicativo FastAPI, inclui os roteadores `healthcheck.router` e `ocr.router` e define os eventos de inicialização e desligamento do aplicativo.

### models.py

O arquivo `models.py` contém a definição dos modelos de dados utilizados na API. Ele define duas classes: `Coordinate` e `BoundingBox`. A classe `Coordinate` representa as coordenadas `x` e `y` de um ponto. A classe `BoundingBox` representa os quatro cantos de uma caixa delimitadora, definidos pelas coordenadas dos cantos superior esquerdo, superior direito, inferior direito e inferior esquerdo. Além disso, o arquivo define as classes `DetectedText` e `DetectedTextResponse` que representam os resultados do OCR.

### ocr.py

O arquivo `ocr.py` contém a implementação da rota da API relacionada ao reconhecimento óptico de caracteres (OCR). Ele importa as bibliotecas necessárias, define a função `recognize()` que realiza o reconhecimento de dígitos em uma imagem e define as rotas `/` e `/upload` da API. A rota `/` retorna o número atual armazenado no banco de dados. A rota `/upload` recebe um arquivo de imagem, salva-o no diretório de upload, realiza o reconhecimento de dígitos na imagem e armazena o número reconhecido no banco de dados.



### requirements.txt

O arquivo `requirements.txt` lista todas as dependências necessárias para executar a API. Essas dependências podem ser instaladas através do comando `pip install -r requirements.txt`.


# Frontend

Um frontend foi construído para que os usuários possam acompanhar o último número chamado a partir de um website.
A stack do frontend é composta por ReactJs, NextJs e TailwindCss.

O repositório do frontend pode ser encontrado [aqui](https://github.com/andrebrito16/queue-sense-frontend).

### Pontos de melhoria

Atualmente a API disponibiliza o recurso de websocket, porém o mesmo não está sendo utilizado no frontend. As requisicões são feitas a cada 1 segundo pelo cliente. O ideal seria utilizar o websocket para que o servidor envie as atualizacões para o cliente, evitando assim o uso desnecessário de recursos.

# Vídeo de Demonstração do Projeto
