#include <grpcpp/grpcpp.h>
#include "../grpc/command.pb.h"
#include "../grpc/command.grpc.pb.h"
#include "../base64/base64.hpp"

class ManageResponseOutput{
    
    public:
        ManageResponseOutput();
        void lsout(terminal::ComandoResponse response);
        void upout(terminal::ComandoResponse response);
        void downout(terminal::ComandoResponse response);
        void cdout(terminal::ComandoResponse response);
        void exiout(terminal::ComandoResponse response);
        void rmout(terminal::ComandoResponse response);
        void lastlogout(terminal::ComandoResponse response);
        void mkdirout(terminal::ComandoResponse response);
};