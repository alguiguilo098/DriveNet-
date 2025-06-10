# DriveNet
 Aplicação de terminal que permite ao usuário interagir com o Google Drive diretamente pela linha de comando, realizando ações como upload, download, listagem de arquivos, criação de pastas, entre outras funcionalidades. 
 
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
