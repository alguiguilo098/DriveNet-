#include "utils/drivenet/Drivenet.hpp"
#include <iostream>
#include <unistd.h>

int main(int argc, const char** argv) {
    ManageResponseOutput out;
    Drivenet cliente(argv[1],out);
    cliente.run();
    return 0;
}

