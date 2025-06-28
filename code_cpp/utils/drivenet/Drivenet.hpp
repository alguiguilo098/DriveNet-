#include <grpcpp/grpcpp.h>
#include "../grpc/command.pb.h"
#include "../grpc/command.grpc.pb.h"
#include "../base64/base64.hpp"
class Drivenet
{
private:
    std::shared_ptr<grpc::Channel> channel;
    std::unique_ptr<terminal::TerminalService::Stub> stub_;
    
    void welcome();
    void help();
    terminal::ComandoResponse drivenet(terminal::ComandoRequest &request, std::string* hash_ptr,std::string* name_ptr);
    terminal::ComandoResponse  exit(terminal::ComandoRequest&request);
    terminal::ComandoResponse downet(terminal::ComandoRequest& request,const std::string& dirdowndload);
    terminal::ComandoResponse upnet(terminal::ComandoRequest& request);
    terminal::ComandoResponse lastlog(terminal::ComandoRequest& request);
    terminal::ComandoResponse lsnet(terminal::ComandoRequest& request);
    terminal::ComandoResponse cdnet(terminal::ComandoRequest& request);
    terminal::ComandoResponse mkdirnet(terminal::ComandoRequest& request);
    terminal::ComandoResponse rmnet(terminal::ComandoRequest& request);
    public:
    void run();

    
    Drivenet(const std::string& server_address);
    ~Drivenet();
};
