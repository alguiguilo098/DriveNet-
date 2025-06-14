#include "Drivenet.hpp"
using namespace std;
void Drivenet::welcome(){
    system("figlet 'DRIVENET'");
    cout <<endl;
}

void Drivenet::help()
{
}

terminal::ComandoResponse Drivenet::lsnet(terminal::ComandoRequest request)
{
    return terminal::ComandoResponse();
}

terminal::ComandoRequest Drivenet::cdnet(terminal::ComandoRequest request)
{
    return terminal::ComandoRequest();
}

terminal::ComandoResponse Drivenet::mkdirnet(terminal::ComandoRequest request)
{
    return terminal::ComandoResponse();
}

terminal::ComandoRequest Drivenet::rmnet(terminal::ComandoRequest request)
{
    return terminal::ComandoRequest();
}

terminal::ComandoRequest Drivenet::chmodnet(terminal::ComandoRequest request)
{
    return terminal::ComandoRequest();
}

Drivenet::Drivenet()
{

}

Drivenet::~Drivenet()
{
}
