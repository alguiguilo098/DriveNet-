#include "Drivenet.hpp"
#include <iostream>
#include <string>
#include <cstdio>
#include <sstream>
#include <vector>
#include <algorithm>

Drivenet::Drivenet(const std::string& server_address) {
    channel = grpc::CreateChannel(server_address, grpc::InsecureChannelCredentials());
    stub_ = terminal::TerminalService::NewStub(channel);
    std::cout<< "conexão criada"<<std::endl;
}

Drivenet::~Drivenet() {}

void Drivenet::welcome() {
    system("figlets Drivenet");
}


void Drivenet::help() {
    FILE* fp = popen("less", "w");
    if (!fp) {
        std::cerr << "Erro ao abrir less\n";
        return;
    }

    fprintf(fp, "Comandos disponíveis:\n\n");

    fprintf(fp, "  drivenet <root_id> <path_credenciais>\n");
    fprintf(fp, "    - Inicia a sessão com as credenciais em base64\n\n");

    fprintf(fp, "  lsnet <hash>\n");
    fprintf(fp, "    - Lista os arquivos do diretório atual\n\n");

    fprintf(fp, "  cdnet <nome_diretorio> <hash>\n");
    fprintf(fp, "    - Muda para o diretório especificado\n\n");

    fprintf(fp, "  mkdirnet <nome_diretorio> <hash>\n");
    fprintf(fp, "    - Cria um novo diretório\n\n");

    fprintf(fp, "  rmnet <nome_arquivo_ou_diretorio> <hash>\n");
    fprintf(fp, "    - Remove um arquivo ou diretório\n\n");

    fprintf(fp, "  upnet <nome_arquivo> <arquivo_em_base64> <hash>\n");
    fprintf(fp, "    - Faz upload de um arquivo codificado em base64\n\n");

    fprintf(fp, "  downet <nome_arquivo> <hash>\n");
    fprintf(fp, "    - Faz download de um arquivo (resposta em base64)\n\n");

    fprintf(fp, "  lastlog <quantidade> <hash>\n");
    fprintf(fp, "    - Exibe os últimos logs de operações\n\n");

    fprintf(fp, "  exit <hash>\n");
    fprintf(fp, "    - Encerra a sessão com o servidor\n\n");

    pclose(fp);
}

void Drivenet::run() {
    std::string linha, hash_cliente, nome_temp;

    while (true) {
        std::cout<<"drivenet"<< "> ";
        std::getline(std::cin, linha);

        if (linha.empty()) continue;

        std::istringstream iss(linha);
        std::vector<std::string> tokens;
        std::string token;

        while (iss >> token)
            tokens.push_back(token);

        if (tokens.empty()) continue;

        std::string comando = tokens[0];
        std::transform(comando.begin(), comando.end(), comando.begin(), ::tolower);

        terminal::ComandoRequest req;
        terminal::ComandoResponse res;
        req.set_comando(comando);

        for (size_t i = 1; i < tokens.size(); ++i)
            req.add_argumentos(tokens[i]);

        if (comando == "?") {
            help();
        } else if (comando == "drivenet") {
            if (tokens.size() < 3) {
                std::cout << "Uso: drivenet <root_id> <path_credenciais>\n";
                continue;
            }
            res = drivenet(req, &hash_cliente, &nome_temp);
        } else if (comando == "exit") {
            req.set_hash_cliente(hash_cliente);
            res = exit(req);
            break;
        } else if (comando == "lsnet") {
            req.set_hash_cliente(hash_cliente);
            res = lsnet(req);
        } else if (comando == "cdnet") {
            req.set_hash_cliente(hash_cliente);
            res = cdnet(req);
        } else if (comando == "mkdirnet") {
            req.set_hash_cliente(hash_cliente);
            res = mkdirnet(req);
        } else if (comando == "rmnet") {
            req.set_hash_cliente(hash_cliente);
            res = rmnet(req);
        } else if (comando == "lastlog") {
            req.set_hash_cliente(hash_cliente);
            res = lastlog(req);
        } else if (comando == "upnet") {
            req.set_hash_cliente(hash_cliente);
            res = upnet(req);
        } else if (comando == "downet") {
            req.set_hash_cliente(hash_cliente);
            res = downet(req, "./code_cpp/FileSystem");  // você pode ajustar o diretório
        }else if (comando == "clear") {
            #ifdef _WIN32
                system("cls");
            #else
                system("clear");
            #endif
        }else {
            std::cout << "Comando desconhecido.\n";
            continue;
        }

        if (!res.erro().empty())
            std::cerr << "Erro: " << res.erro() << std::endl;
    }

}


terminal::ComandoResponse Drivenet::drivenet(terminal::ComandoRequest &request, std::string* hash_ptr,std::string* name_ptr) {
    terminal::ComandoRequest req;
    terminal::ComandoResponse response;
    grpc::ClientContext context;

    std::string root_id = request.argumentos(0);
    std::string cred_path = request.argumentos(1);

    std::vector<unsigned char> cred_bytes = read_file(cred_path);
    std::string cred_base64 = base64_encode(cred_bytes);

    req.set_comando("drivenet");
    req.add_argumentos(root_id);
    req.add_argumentos(cred_base64);

    grpc::Status status = stub_->ExecutarComando(&context, req, &response);

    if (!status.ok()) {
        response.add_saida("Erro de comunicação gRPC: " + status.error_message());
        response.set_codigo_saida(-10);
        return response;
    }

    if (response.saida_size() > 0) {
        std::string result = response.saida(0); // Ex: "HASH123,arquivo.json"
        size_t pos = result.find(',');

        if (pos != std::string::npos) {
            std::string hash_cliente = result.substr(0, pos);
            std::string nome_temp = result.substr(pos + 1);

            std::cout << "Sessão iniciada:\nHash Cliente: " << hash_cliente << "\nArquivo temporário: " << nome_temp << "\n";

            // Seta o ponteiro se for válido
            if (hash_ptr) {
                *hash_ptr = hash_cliente;
                *name_ptr= nome_temp;
            }

            request.set_hash_cliente(hash_cliente); // opcional: atualiza request original
        } else {
            response.add_saida("Formato inválido da resposta.");
            response.set_codigo_saida(-11);
        }
    } else {
        response.add_saida("Nenhuma resposta do servidor.");
        response.set_codigo_saida(-12);
    }

    return response;
}


terminal::ComandoResponse Drivenet::exit(terminal::ComandoRequest& req) {
    grpc::ClientContext context;
    terminal::ComandoResponse response;

    grpc::Status status = stub_->ExecutarComando(&context, req, &response);

    if (status.ok()) {
        std::cout << "Sessão finalizada com sucesso no servidor.\n";
    } else {
        std::cerr << "Erro ao finalizar sessão: " << status.error_message() << std::endl;
        response.add_saida("Erro de comunicação gRPC: " + status.error_message());
        response.set_codigo_saida(-10);
    }
    return response;
}



terminal::ComandoResponse Drivenet::downet(terminal::ComandoRequest &request,const std::string& dirdowndload){
    grpc::ClientContext context;
    terminal::ComandoResponse response;
    grpc::Status status = stub_->ExecutarComando(&context, request, &response);
    if (!status.ok()) {
        response.set_erro("Erro ao executar downet: " + status.error_message());
        response.set_codigo_saida(-1);
        return response;
    }
    auto base=response.saida(0);
    auto bytes=base64_decode(base);
    write_file("calvo.txt",bytes);

    return response;
}

terminal::ComandoResponse Drivenet::upnet(terminal::ComandoRequest &request){
    grpc::ClientContext context;
    terminal::ComandoResponse response;

    std::string path_file=request.argumentos(1);
    auto bytes=read_file(path_file);
    std::cout << "Bytes lidos: " << bytes.size() << "\n";

    std::string base64=base64_encode(bytes);

    path_file = request.argumentos(1);
    std::cout << base64<<std::endl;
    request.mutable_argumentos()->DeleteSubrange(1, 1);
    request.add_argumentos(base64);

    grpc::Status status = stub_->ExecutarComando(&context, request, &response);
    if (!status.ok()) {
        response.set_erro("Erro ao executar downet: " + status.error_message());
        response.set_codigo_saida(-1);
        return response;
    }
    return response;
}

terminal::ComandoResponse Drivenet::lsnet(terminal::ComandoRequest& request) {
    grpc::ClientContext context;
    terminal::ComandoResponse response;
    grpc::Status status = stub_->ExecutarComando(&context, request, &response);

    if (!status.ok()) {
        response.set_erro("Erro ao executar lsnet: " + status.error_message());
        response.set_codigo_saida(-1);
    }

    return response;
}

terminal::ComandoResponse Drivenet::cdnet(terminal::ComandoRequest& request) {
    grpc::ClientContext context;
    terminal::ComandoResponse response;
    grpc::Status status = stub_->ExecutarComando(&context, request, &response);

    if (!status.ok()) {
        response.set_erro("Erro ao executar cdnet: " + status.error_message());
        response.set_codigo_saida(-1);
    }

    return response;
}

terminal::ComandoResponse Drivenet::mkdirnet(terminal::ComandoRequest& request) {
    grpc::ClientContext context;
    terminal::ComandoResponse response;
    grpc::Status status = stub_->ExecutarComando(&context, request, &response);

    if (!status.ok()) {
        response.set_erro("Erro ao executar mkdirnet: " + status.error_message());
        response.set_codigo_saida(-1);
    }

    return response;
}

terminal::ComandoResponse Drivenet::rmnet(terminal::ComandoRequest& request) {
    grpc::ClientContext context;
    terminal::ComandoResponse response;
    grpc::Status status = stub_->ExecutarComando(&context, request, &response);

    if (!status.ok()) {
        response.set_erro("Erro ao executar rmnet: " + status.error_message());
        response.set_codigo_saida(-1);
    }

    return response;
}

terminal::ComandoResponse Drivenet::lastlog(terminal::ComandoRequest& request) {
    grpc::ClientContext context;
    terminal::ComandoResponse response;

    grpc::Status status = stub_->ExecutarComando(&context, request, &response);
    if (!status.ok()) {
        response.set_erro("Erro ao executar chmodnet: " + status.error_message());
        response.set_codigo_saida(-1);
    }    
    return response;
}

