#include <grpcpp/grpcpp.h>
#include "../grpc/command.pb.h"
#include "../grpc/command.grpc.pb.h"
#include "../base64/base64.hpp"

class ManageResponseOutput{
    
    public:
        ManageResponseOutput();
        void lsout(terminal::ComandoResponse response);
        void lastlogout(terminal::ComandoResponse response);
        void mkdirout(terminal::ComandoResponse response);
};