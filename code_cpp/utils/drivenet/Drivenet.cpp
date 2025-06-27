#include "Drivenet.hpp"
#include <iostream>
#include <string>

Drivenet::Drivenet(const std::string& server_address) {
    channel = grpc::CreateChannel(server_address, grpc::InsecureChannelCredentials());
    stub_ = terminal::TerminalService::NewStub(channel);
    std::cout<< "conexão criada"<<std::endl;
}

Drivenet::~Drivenet() {}

void Drivenet::welcome() {
    std::cout << "Bem-vindo ao DriveNet!\n";
}

void Drivenet::help() {
    std::cout << "Comandos disponíveis: lsnet, cdnet, mkdirnet, rmnet, chmodnet, lastlog\n";
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
    write_file(dirdowndload,bytes);

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

terminal::ComandoResponse Drivenet::chmodnet(terminal::ComandoRequest& request) {
    grpc::ClientContext context;
    terminal::ComandoResponse response;
    grpc::Status status = stub_->ExecutarComando(&context, request, &response);

    if (!status.ok()) {
        response.set_erro("Erro ao executar chmodnet: " + status.error_message());
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

