#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <string>

std::string base64_encode(const std::vector<unsigned char>& bytes);
std::vector<unsigned char> base64_decode(const std::string& encoded);
std::vector<unsigned char> read_file(const std::string& filename);
void write_file(const std::string& filename, const std::vector<unsigned char>& data);