#include "command.pb.h"
class Drivenet
{
public:
    void welcome();
    void help();
    terminal::ComandoResponse lsnet(terminal::ComandoRequest request);
    terminal::ComandoRequest cdnet(terminal::ComandoRequest request);
    terminal::ComandoResponse mkdirnet(terminal::ComandoRequest request);
    terminal::ComandoRequest rmnet(terminal::ComandoRequest request);
    terminal::ComandoRequest chmodnet(terminal::ComandoRequest request);

    Drivenet(/* args */);
    ~Drivenet();
};

