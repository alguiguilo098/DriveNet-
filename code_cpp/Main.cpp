#include "utils/drivenet/Drivenet.hpp"
#include <iostream>

int main() {
    Drivenet client("127.0.0.1:50051");

    client.welcome();
    client.help();

    terminal::ComandoRequest request;
    request.set_comando("cdnet");
    request.add_argumentos("cal");
    terminal::ComandoResponse response = client.cdnet(request);
    
    
    for (size_t i = 0; i < response.saida_size(); i++){
        std::cout<< response.saida(i)<<std::endl<<std::endl;
    }
    terminal::ComandoRequest request1;
    request.set_comando("lsnet");
    terminal::ComandoResponse response1 = client.lsnet(request);

    for (size_t i = 0; i < response1.saida_size(); i++){
        std::cout<< response1.saida(i)<<std::endl<<std::endl;
    }
    
    std::cout<<"print";

    

    return 0;
}
