# DriveNet
 Aplicação de terminal que permite ao usuário interagir com o Google Drive diretamente pela linha de comando, realizando ações como upload, download, listagem de arquivos, criação de pastas, entre outras funcionalidades. 
 
## ⚙️ Configuração do Ambiente (gRPC + Protobuf em C++)

### Requisitos

Certifique-se de ter os seguintes pacotes instalados no sistema:

```bash
sudo dnf install -y gcc-c++ make cmake git autoconf libtool pkgconf-pkg-config
```

Ou instale os equivalentes de acordo com sua distribuição.

---

### Instalação do gRPC + Protobuf + Plugin C++

```bash
# Clone o repositório oficial do gRPC com submódulos
git clone --recurse-submodules -b v1.48.0 https://github.com/grpc/grpc
cd grpc

# Crie diretório de build
mkdir -p cmake/build
cd cmake/build

# Configure o CMake com instalação habilitada
cmake ../.. \
  -DgRPC_INSTALL=ON \
  -DgRPC_BUILD_TESTS=OFF \
  -DCMAKE_INSTALL_PREFIX=/usr/local

# Compile e instale
make -j$(nproc)
sudo make install
sudo ldconfig
```

---

### Verificação

Após a instalação:

```bash
protoc --version             # deve mostrar a mesma versão usada no projeto (ex: 3.19.6)
which grpc_cpp_plugin        # deve mostrar: /usr/local/bin/grpc_cpp_plugin
```

---

### 🛠️ Gerando os arquivos do Protobuf

```bash
protoc \
  -I. \
  --cpp_out=. \
  --grpc_out=. \
  --plugin=protoc-gen-grpc=/usr/local/bin/grpc_cpp_plugin \
  seu_arquivo.proto
```

---

### 🧱 Compilando o projeto (exemplo com g++)

```bash
g++ -std=c++17 main.cpp seu_arquivo.pb.cc seu_arquivo.grpc.pb.cc \
  -I/usr/local/include \
  -L/usr/local/lib \
  -lprotobuf -lgrpc++ -lpthread \
  -o app
```
