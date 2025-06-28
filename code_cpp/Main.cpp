#include "utils/drivenet/Drivenet.hpp"
#include "utils/base64.hpp"
#include <iostream>

int main(int argc, const char** argv) {
    Drivenet cliente("localhost:50051");

    terminal::ComandoRequest request;  // ✅ Correto
    request.set_comando("downet");
    request.add_argumentos("upload.txt");

    terminal::ComandoResponse response = cliente.downet(request,".");  // ✅ passa como referência automaticamente

    for (const auto& linha : response.saida()) {
        std::cout << linha << std::endl;
    }

    return 0;
}
