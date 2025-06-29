#include "utils/drivenet/Drivenet.hpp"
#include <iostream>
#include <unistd.h>

int main(int argc, const char** argv) {
    Drivenet cliente(argv[1]);
    cliente.run();
    return 0;
}

