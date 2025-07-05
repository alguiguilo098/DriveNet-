
#include<iostream>
#include<string>
#include"base64.hpp"
const std::string base64_chars =
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    "abcdefghijklmnopqrstuvwxyz"
    "0123456789+/";
    
std::string base64_encode(const std::vector<unsigned char>& bytes) {
    std::string encoded;
    int i = 0;
    unsigned char char_array_3[3];
    unsigned char char_array_4[4];

    for (size_t pos = 0; pos < bytes.size(); ++pos) {
        char_array_3[i++] = bytes[pos];
        if (i == 3) {
            char_array_4[0] =  (char_array_3[0] & 0xfc) >> 2;
            char_array_4[1] = ((char_array_3[0] & 0x03) << 4) + ((char_array_3[1] & 0xf0) >> 4);
            char_array_4[2] = ((char_array_3[1] & 0x0f) << 2) + ((char_array_3[2] & 0xc0) >> 6);
            char_array_4[3] =   char_array_3[2] & 0x3f;

            for (i = 0; i < 4; ++i)
                encoded += base64_chars[char_array_4[i]];
            i = 0;
        }
    }

    if (i) {
        for (int j = i; j < 3; ++j)
            char_array_3[j] = '\0';

        char_array_4[0] =  (char_array_3[0] & 0xfc) >> 2;
        char_array_4[1] = ((char_array_3[0] & 0x03) << 4) + ((char_array_3[1] & 0xf0) >> 4);
        char_array_4[2] = ((char_array_3[1] & 0x0f) << 2) + ((char_array_3[2] & 0xc0) >> 6);
        char_array_4[3] =   char_array_3[2] & 0x3f;

        for (int j = 0; j < i + 1; ++j)
            encoded += base64_chars[char_array_4[j]];
        while (i++ < 3)
            encoded += '=';
    }

    return encoded;
}

std::vector<unsigned char> base64_decode(const std::string& encoded) {
    std::vector<unsigned char> decoded;
    int i = 0;
    unsigned char char_array_4[4], char_array_3[3];
    int in_len = encoded.size(), pos = 0;

    auto is_base64 = [](unsigned char c) {
        return (isalnum(c) || (c == '+') || (c == '/'));
    };

    while (in_len-- && is_base64(encoded[pos])) {
        char_array_4[i++] = encoded[pos]; pos++;
        if (i == 4) {
            for (i = 0; i < 4; ++i)
                char_array_4[i] = base64_chars.find(char_array_4[i]);

            char_array_3[0] = ( char_array_4[0] << 2       ) + ((char_array_4[1] & 0x30) >> 4);
            char_array_3[1] = ((char_array_4[1] & 0xf) << 4) + ((char_array_4[2] & 0x3c) >> 2);
            char_array_3[2] = ((char_array_4[2] & 0x3) << 6) +   char_array_4[3];

            for (i = 0; i < 3; ++i)
                decoded.push_back(char_array_3[i]);
            i = 0;
        }
    }

    if (i) {
        for (int j = i; j < 4; ++j)
            char_array_4[j] = 0;

        for (int j = 0; j < 4; ++j)
            char_array_4[j] = base64_chars.find(char_array_4[j]);

        char_array_3[0] = ( char_array_4[0] << 2       ) + ((char_array_4[1] & 0x30) >> 4);
        char_array_3[1] = ((char_array_4[1] & 0xf) << 4) + ((char_array_4[2] & 0x3c) >> 2);
        char_array_3[2] = ((char_array_4[2] & 0x3) << 6) +   char_array_4[3];

        for (int j = 0; j < i - 1; ++j)
            decoded.push_back(char_array_3[j]);
    }

    return decoded;
}

// Lê um arquivo e retorna os bytes
std::vector<unsigned char> read_file(const std::string& filename) {
    std::ifstream file(filename, std::ios::binary);
    return std::vector<unsigned char>(std::istreambuf_iterator<char>(file), {});
}

// Escreve os bytes em um novo arquivo
void write_file(const std::string& filename, const std::vector<unsigned char>& data) {
    std::ofstream file(filename, std::ios::binary);
    if (!file) {
        std::cerr << "Erro ao abrir o arquivo para escrita: " << filename << "\n";
        return;
    }
    file.write(reinterpret_cast<const char*>(data.data()), data.size());
    file.flush();
}