# DriveNet-
 Aplicação de terminal que permite ao usuário interagir com o Google Drive diretamente pela linha de comando, realizando ações como upload, download, listagem de arquivos, criação de pastas, entre outras funcionalidades. 
## Arquitetura
![image](https://github.com/user-attachments/assets/5aa41504-a526-4185-8f86-0f9a8c4a3451)
* **Grpc**:Comunição entre o programa de terminal e o servidor python.
* **redis**: Serviço de cache para manter os arquivos mais recentes
* **pymongo**: Operações de logs de deletar e acesso ao arquivos.
* **pyDrive**: API de google drive para manipular arquivos.

## Interface de Serviço

A interface gRPC `TerminalService` possui um método chamado `ExecutarComando`, que permite enviar um comando com seus argumentos para o servidor e receber a resposta da execução.
A requisição (`ComandoRequest`) contém o nome do comando, uma lista de argumentos em texto e um identificador de sessão (`hash_cliente`).
A resposta (`ComandoResponse`) traz a saída padrão do comando, uma mensagem de erro caso exista, e um código de saída que indica se a execução foi bem-sucedida ou não.
Essa interface permite executar comandos remotamente e obter seus resultados de forma simples e eficiente.

---

## Comandos do Servidor (`DriveNetServer`)

### `drivenet`

* **Função**: Inicia a sessão do cliente no servidor com credenciais codificadas em base64.
* **Argumento**: ID da pasta raiz, conteúdo do arquivo de credenciais em base64
* **Retorno**: `hash_cliente`, nome temporário do arquivo salvo
* **Código**: `0` (sessão iniciada)

---

### `mkdirnet`

* **Função**: Cria um diretório no Google Drive
* **Argumento**: nome do diretório, hash cliente
* **Retorno**: mensagem de sucesso ou erro
* **Código**: `1` (sucesso), `-1` (erro)

---

### `cdnet`

* **Função**: Muda o diretório atual no Drive
* **Argumento**: nome, hash cliente
* **Retorno**: mensagem de status
* **Código**: `4` (sucesso), `-4` (erro)

---

### `rmnet`

* **Função**: Remove arquivo ou pasta
* **Argumento**: nome, hash cliente
* **Retorno**: mensagem de status
* **Código**: `3` (sucesso), `-3` (erro)

---

### `upnet`

* **Função**: Faz upload de um arquivo em base64
* **Argumentos**: nome do arquivo, conteúdo em base64, hash cliente
* **Retorno**: mensagem de sucesso ou erro
* **Código**: `5` (sucesso), `-5` (erro)

---

### `downet`

* **Função**: Faz download de arquivo em base64
* **Argumento**: nome, hash cliente
* **Retorno**: conteúdo em base64 ou mensagem de erro
* **Código**: `6` (sucesso), `-6` (erro)

---

### `lsnet`

* **Função**: Lista arquivos no diretório atual
* **Argumento**: hash cliente
* **Retorno**: lista com ID, nome, tamanho, tipo e data
* **Código**: `2` (sucesso), `-2` (erro)

---

### `lastlog`

* **Função**: Retorna os últimos logs
* **Argumento**: quantidade de logs, hash cliente
* **Retorno**: lista com timestamp, mensagem e status
* **Código**: `7` (sucesso implícito)

---

### `exit`

* **Função**: Encerra a sessão atual e remove as credenciais
* **Argumento**: hash cliente
* **Retorno**: sessão encerrada (sem mensagem obrigatória)
* **Código**: `10` (sucesso, sugerido), `-10` (erro)

---

### Comando inválido

* **Função**: Comando não reconhecido
* **Retorno**: mensagem padrão `"Comando não reconhecido"`
* **Código**: `-99` (sugerido)


## Configuração do Ambiente

### 1. Subindo Redis e MongoDB com Docker

Para facilitar a configuração do ambiente, utilize o Docker Compose para subir os serviços necessários:

```bash
docker compose up -d
```


### 2. Instalação do gRPC

O projeto utiliza gRPC nas linguagens Python e C++. Para configurá-lo corretamente, siga as instruções oficiais de instalação:

* **gRPC para Python**:
  [Guia Rápido - gRPC Python](https://grpc.io/docs/languages/python/quickstart/)

* **gRPC para C++**:
  [Guia Rápido - gRPC C++](https://grpc.io/docs/languages/cpp/quickstart/)


### 3. Gerar Arquivos grpc em C++ 
```bash
cd code_cpp/
make
```

### 4. Gerar Arquivos grpc em python 
```bash
cd code_python/
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. command.proto
```

### 5. Instalação das Dependências do Python
Instale as dependências necessárias para o servidor Python:

```bash
pip install -r requirements.txt
```

## Configuração credencias google Drive 

