#include "utils/drivenet/Drivenet.hpp"
#include <iostream>
#include "utils/base64.hpp"

int main(int argc, char const *argv[])
{
    auto file_byte=read_file("./teste.txt");
    auto base64=base64_encode(file_byte);
    auto file_a=base64_decode(base64);
    write_file("teste2.txt",file_a);
    std::cout<< base64<<std::endl;
    
    return 0;
}



