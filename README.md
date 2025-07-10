# DriveNet-
 Aplicação de terminal que permite ao usuário interagir com o Google Drive diretamente pela linha de comando, realizando ações como upload, download, listagem de arquivos, criação de pastas, entre outras funcionalidades. 
## Arquitetura

![image](https://github.com/user-attachments/assets/93df7a6e-4a0d-4f36-b7e3-df453a72c317)

* **Grpc**:Comunição entre o programa de terminal e o servidor python.
* **redis**: Serviço de cache para manter os arquivos mais recentes
* **pymongo**: Operações de logs de deletar e acesso ao arquivos.
* **pyDrive**: API de google drive para manipular arquivos.
* **replicação**: Serviço de replicação usando o mongo-arbitrary 

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
* **Argumento**: nome do diretório
* **Hash cliente**: hash gerada na autenticação
* **Retorno**: mensagem de sucesso ou erro
* **Código**: `1` (sucesso), `-1` (erro)

---

### `cdnet`

* **Função**: Muda o diretório atual no Drive
* **Argumento**: nome
* **Hash cliente**: hash gerada na autenticação
* **Retorno**: mensagem de status
* **Código**: `4` (sucesso), `-4` (erro)

---

### `rmnet`

* **Função**: Remove arquivo ou pasta
* **Argumento**: nome
* **Hash cliente**: hash gerada na autenticação
* **Retorno**: mensagem de status
* **Código**: `3` (sucesso), `-3` (erro)

---

### `upnet`

* **Função**: Faz upload de um arquivo em base64
* **Argumentos**: nome do arquivo, conteúdo em base64
* **Hash cliente**: hash gerada na autenticação
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
* **Código**: `7` (sucesso) e `-7` error

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

Claro! Aqui está uma versão mais organizada, clara e visualmente agradável para o README da configuração das credenciais do Google Drive:

---

# Configuração das Credenciais para Google Drive API

Este guia passo a passo mostra como criar e configurar as credenciais necessárias para acessar a API do Google Drive via script.

---

## Passo 1: Acesse o Google Cloud Console

* Faça login com sua conta Google em [https://console.cloud.google.com](https://console.cloud.google.com).

---

## Passo 2: Crie um Projeto

* No menu superior, clique em **Selecionar projeto** > **Novo Projeto**.
* Dê um nome ao projeto.
* Clique em **Criar**.

---

## Passo 3: Ative a API do Google Drive

* No painel do projeto, acesse **APIs e serviços** > **Biblioteca**.
* Busque por **Google Drive API**.
* Clique na API e depois em **Ativar**.

---

## Passo 4: Crie as Credenciais

* Vá para **APIs e serviços** > **Credenciais**.
* Clique em **Criar credenciais** > **ID do cliente OAuth**.

> Caso seja solicitado, configure a tela de consentimento:
>
> * Selecione o tipo **Externo**.
> * Preencha os campos obrigatórios (nome do app, e-mail de suporte, etc).
> * Salve a configuração.

* Escolha o tipo de aplicativo: **Aplicativo de área de trabalho (Desktop app)**.
* Dê um nome para as credenciais (ex: `Credenciais Drive`).
* Clique em **Criar**.

---

## Passo 5: Baixe o arquivo `credentials.json`

* Após criar, faça o download do arquivo `.json`.
* Salve-o na pasta do seu projeto.
* Se necessário, renomeie para `credentials.json`.

---

## Passo 6: Compartilhe arquivos/pastas com a Conta de Serviço

* Abra o arquivo `credentials.json` e copie o e-mail da conta de serviço (geralmente termina com `@<projeto>.iam.gserviceaccount.com`).
* No Google Drive, clique com o botão direito no arquivo ou pasta que deseja acessar via script.
* Selecione **Compartilhar**.
* Cole o e-mail copiado no campo de compartilhamento.
* Defina a permissão como **Visualizador** ou **Editor** (conforme necessário).
* Clique em **Enviar**.

