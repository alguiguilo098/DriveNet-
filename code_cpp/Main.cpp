#include "utils/drivenet/Drivenet.hpp"
#include <iostream>

int main() {
    Drivenet client("127.0.0.1:50051");

    client.welcome();
    client.help();

    terminal::ComandoRequest request;
    request.set_comando("lastlog");
    request.add_argumentos("3");

    terminal::ComandoResponse response = client.lastlog(request);

    return 0;
}
