#include "ManageResponse.hpp"

#include <iostream>
#include <sstream>
#include <vector>
#include <iomanip>
#include "../grpc/command.pb.h"
#include "../grpc/command.grpc.pb.h"
#include <sstream>
#include <string>
#include <iomanip>
#include <vector>
#include <cstdio>

ManageResponseOutput::ManageResponseOutput()
{
}


void ManageResponseOutput::lsout(terminal::ComandoResponse response)
{
    FILE* fp = popen("less -R", "w");
    if (!fp) {
        std::cerr << "Erro ao abrir less\n";
        return;
    }

    // Cabeçalho
    fprintf(fp, "%-25s %-30s %-10s %-20s %-25s\n", "ID", "Nome", "Tamanho", "MIME Type", "Modificado");
    fprintf(fp, "%s\n", std::string(110, '-').c_str());

    for (const auto& line : response.saida()) {
        std::istringstream linestream(line);
        std::string id, name, size, mime, modified;

        std::getline(linestream, id, ',');
        std::getline(linestream, name, ',');
        std::getline(linestream, size, ',');
        std::getline(linestream, mime, ',');
        std::getline(linestream, modified, ',');

        fprintf(fp, "%-25s %-30s %-10s %-20s %-25s\n",
                id.c_str(), name.c_str(), size.c_str(), mime.c_str(), modified.c_str());
    }

    pclose(fp);
}




void ManageResponseOutput::upout(terminal::ComandoResponse response)
{
}

void ManageResponseOutput::downout(terminal::ComandoResponse response)
{
}

void ManageResponseOutput::cdout(terminal::ComandoResponse response)
{
}

void ManageResponseOutput::exiout(terminal::ComandoResponse response)
{
}

void ManageResponseOutput::rmout(terminal::ComandoResponse response)
{
}

void ManageResponseOutput::lastlogout(terminal::ComandoResponse response)
{
}

void ManageResponseOutput::mkdirout(terminal::ComandoResponse response)
{
}


