# DriveNet-
 Aplicação de terminal que permite ao usuário interagir com o Google Drive diretamente pela linha de comando, realizando ações como upload, download, listagem de arquivos, criação de pastas, entre outras funcionalidades. 
## Arquitetura
![image](https://github.com/user-attachments/assets/5aa41504-a526-4185-8f86-0f9a8c4a3451)
* **Grpc**:Comunição entre o programa de terminal e o servidor python.
* **redis**: Serviço de cache para manter os arquivos mais recentes
* **pymongo**: Operações de logs de deletar e acesso ao arquivos.
* **pyDrive**: API de google drive para manipular arquivos.

## Interface de Serviço
```bash
syntax = "proto3";

package terminal;

// Serviço de terminal com envio e resposta de comandos
service TerminalService {
  // Envia um comando com argumentos e recebe a saída
  rpc ExecutarComando (ComandoRequest) returns (ComandoResponse);
}

// Mensagem para enviar um comando com argumentos
message ComandoRequest {
  string comando = 1;            // Ex: "ls"
  repeated string argumentos = 2; // Ex: ["-la", "/home/user"]
}

// Mensagem com a resposta do comando
message ComandoResponse {
  string saida = 1;              // Saída padrão (stdout)
  string erro = 2;               // Saída de erro (stderr)
  int32 codigo_saida = 3;       // Código de saída do processo
}

```
* **Cliente(C++)**: O cliente pode somente acessar do servidor,  O CommandoResponse, com a mensagem de erro, saída do codigo, e o codigo de erro.
* **Servidor(Python)**: O servidor em python pode somente acessar do cliente, ComandoResquest, contendo o a operação e os argumentos da mesma.

### Operações 
   * **?**: Mostras as operações que DriveNet- pode Realizar
   * **mkdirnet**: Criar um diretório do google Drive
   * **cdnet**: Mudar o diretório atual
   * **touchnet**: Cria um arquivo no google Drive 
   * **rmnet**: remover um arquivo do google Drive
   * **chmodnet**: Mudar as permissões do arquivo do google Drive 
   * **lsnet**: listar o diretório atual do google Drive
   * **lastlognet**: mostrar o logs do sistemas
 
### Codigo de Erro
 * **1**:  Arquivo Criado com sucesso
 * **-1**: Erro na criação do Arquivo
 * **2**:  Mudança de diretório feita com sucesso
 * **-2**: Erro na mudança de diretório
 * **3**:  Arquivo Criado com sucesso
 * **-3**: Erro na criação do arquivo
 * **4**:  Remover Arquivo com sucesso
 * **-4**: Erro ao tentar Remover Arquivo
 * **5**:  
## ⚙️ Configuração do Ambiente

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
cd code_cpp/
make 
```
