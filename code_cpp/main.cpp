#include <iostream>
#include "command.pb.h"
int main() {
    // Criando uma requisição de comando
    terminal::ComandoRequest request;
    request.set_comando("ls");
    request.add_argumentos("-la");
    request.add_argumentos("/home");

    // Imprimindo os dados
    std::cout << "Comando: " << request.comando() << std::endl;
    for (int i = 0; i < request.argumentos_size(); ++i) {
        std::cout << "Arg " << i << ": " << request.argumentos(i) << std::endl;
    }

    // Criando uma resposta de comando
    terminal::ComandoResponse response;
    response.set_saida("arquivo1\narquivo2");
    response.set_erro("");
    response.set_codigo_saida(0);

    // Imprimindo a resposta
    std::cout << "\nSaída:\n" << response.saida() << std::endl;
    std::cout << "Erro:\n" << response.erro() << std::endl;
    std::cout << "Código de saída: " << response.codigo_saida() << std::endl;

    return 0;
}
