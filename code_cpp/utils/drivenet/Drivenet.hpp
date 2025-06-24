#include <grpcpp/grpcpp.h>
#include "../grpc/command.pb.h"
#include "../grpc/command.grpc.pb.h"

class Drivenet
{
private:
    std::shared_ptr<grpc::Channel> channel;
    std::unique_ptr<terminal::TerminalService::Stub> stub_;

public:
    void welcome();
    void help();

    terminal::ComandoResponse lastlog(terminal::ComandoRequest& request);
    terminal::ComandoResponse lsnet(terminal::ComandoRequest& request);
    terminal::ComandoResponse cdnet(terminal::ComandoRequest& request);
    terminal::ComandoResponse mkdirnet(terminal::ComandoRequest& request);
    terminal::ComandoResponse rmnet(terminal::ComandoRequest& request);
    terminal::ComandoResponse chmodnet(terminal::ComandoRequest& request);

    Drivenet(const std::string& server_address);
    ~Drivenet();
};
