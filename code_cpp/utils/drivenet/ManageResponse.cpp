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

    // Cabeçalho (sem a coluna ID)
    fprintf(fp, "%-30s %-10s %-20s %-25s\n", "Nome", "Tamanho", "MIME Type", "Modificado");
    fprintf(fp, "%s\n", std::string(90, '-').c_str());

    for (const auto& line : response.saida()) {
        std::istringstream linestream(line);
        std::string id, name, size, mime, modified;

        std::getline(linestream, id, ',');      // ignora o ID
        std::getline(linestream, name, ',');
        std::getline(linestream, size, ',');
        std::getline(linestream, mime, ',');
        std::getline(linestream, modified, ',');

        // Substitui underscores por espaços nos nomes
        std::replace(name.begin(), name.end(), '_', ' ');

        fprintf(fp, "%-30s %-10s %-20s %-25s\n",
                name.c_str(), size.c_str(), mime.c_str(), modified.c_str());
    }

    pclose(fp);
}


void ManageResponseOutput::lastlogout(terminal::ComandoResponse response)
{
    FILE* fp = popen("less -R", "w");
    if (!fp) {
        std::cerr << "Erro ao abrir less\n";
        return;
    }

    fprintf(fp, "Últimos logs de operações:\n\n");

    int index = 1;
    for (const auto& line : response.saida()) {
        fprintf(fp, "%2d. %s\n", index++, line.c_str());
    }

    pclose(fp);
}

void ManageResponseOutput::mkdirout(terminal::ComandoResponse response)
{
}


