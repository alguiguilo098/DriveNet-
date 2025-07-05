#include "Drivenet.hpp"
#include <iostream>
#include <string>
#include <cstdio>
#include <sstream>
#include <vector>
#include <algorithm>

Drivenet::Drivenet(const std::string& server_address,ManageResponseOutput output) {
    output = output;
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

    fprintf(fp, "  lsnet \n");
    fprintf(fp, "    - Lista os arquivos do diretório atual\n\n");

    fprintf(fp, "  cdnet <nome_diretorio>\n");
    fprintf(fp, "    - Muda para o diretório especificado\n\n");

    fprintf(fp, "  mkdirnet <nome_diretorio>\n");
    fprintf(fp, "    - Cria um novo diretório\n\n");

    fprintf(fp, "  rmnet <nome_arquivo_ou_diretorio> \n");
    fprintf(fp, "    - Remove um arquivo ou diretório\n\n");

    fprintf(fp, "  upnet <nome_arquivo> <arquivo_em_base64> \n");
    fprintf(fp, "    - Faz upload de um arquivo codificado em base64\n\n");

    fprintf(fp, "  downet <nome_arquivo> \n");
    fprintf(fp, "    - Faz download de um arquivo (resposta em base64)\n\n");

    fprintf(fp, "  lastlog <quantidade> \n");
    fprintf(fp, "    - Exibe os últimos logs de operações\n\n");

    fprintf(fp, "  exit \n");
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
        }else if (comando == "exit") {
            req.set_hash_cliente(hash_cliente);
            res = exit(req,&nome_temp,&hash_cliente);
            break;
        } else if (!isautenticaded){
            std::cout << "Você precisa autenticarse primeiro com o comando 'drivenet <root_id> <path_credenciais>'\n";
            continue;
        }else if (comando == "lsnet" && this->isautenticaded) {
            req.set_hash_cliente(hash_cliente);
            res = lsnet(req);
            this->output.lsout(res);
        } else if (comando == "cdnet" && this->isautenticaded) {
            req.set_hash_cliente(hash_cliente);
            res = cdnet(req);

        } else if (comando == "mkdirnet" && this->isautenticaded) {
            req.set_hash_cliente(hash_cliente);
            res = mkdirnet(req);
        } else if (comando == "rmnet" && this->isautenticaded) {
            req.set_hash_cliente(hash_cliente);
            res = rmnet(req);
        } else if (comando == "lastlog" && this->isautenticaded) {
            req.set_hash_cliente(hash_cliente);
            res = lastlog(req);
            this->output.lastlogout(res);
        } else if (comando == "upnet" && this->isautenticaded) {
            req.set_hash_cliente(hash_cliente);
            res = upnet(req);
        } else if (comando == "downet" && this->isautenticaded) {
            req.set_hash_cliente(hash_cliente);
            res = downet(req,"/home/galmeidalopes/DriveNet-/FileSystem/"+req.argumentos(0));
        }else if (comando == "clear") {
            #ifdef _WIN32
                system("cls");
            #else
                system("clear");
            #endif
        }else{
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
                *hash_ptr = hash_cliente; // Atualiza o hash do cliente 
                *name_ptr= nome_temp; // Atualiza o nome do arquivo temporário
                this->isautenticaded= true; // Marca que a sessão foi autenticada
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


terminal::ComandoResponse Drivenet::exit(terminal::ComandoRequest& req,std::string* uuid4,std::string* hash_ptr) {
    grpc::ClientContext context;
    terminal::ComandoResponse response;
    if (uuid4) {
        req.add_argumentos(*uuid4);
    }
    if (hash_ptr) {
        req.add_argumentos(*hash_ptr);
    }
    grpc::Status status = stub_->ExecutarComando(&context, req, &response);
    
    if (status.ok()) {
        std::cout <<response.codigo_saida()<<response.saida(0)<<"\n";
        this->isautenticaded=false; // Marca que a sessão foi finalizada
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
    if (bytes.size()>3){
        write_file(dirdowndload,bytes);
        std::cout << "Arquivo baixado com sucesso: "<< request.argumentos(0)<< "\n";
    }else{
        std::cout << "Erro ao baixar o arquivo:" << request.argumentos(0)<< "\n";
    }

    return response;
}

terminal::ComandoResponse Drivenet::upnet(terminal::ComandoRequest &request){
    grpc::ClientContext context;
    terminal::ComandoResponse response;

    std::string path_file=request.argumentos(1);
    auto bytes=read_file(path_file);

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
    }else{
        std::cout << "Arquivo enviado com sucesso: " << path_file << "\n";
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
    }else{
        std::cout << "Diretório alterado com sucesso:" << response.saida(0)<< "\n";
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
    }else{
        std::cout << response.saida(0)<< "\n";
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
    }else{
        std::cout << response.saida(0)<< "\n";
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

