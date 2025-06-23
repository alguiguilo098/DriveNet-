compile:
	@protoc -I ../ --cpp_out=./src ../command.proto
	@protoc -I ../ --grpc_out=./src --plugin=protoc-gen-grpc=`which grpc_cpp_plugin` ../command.proto
	
run:
	@g++ -std=c++17 main.cpp command.pb.cc command.grpc.pb.cc \
    `pkg-config --cflags --libs grpc++` -lprotobuf -lpthread -o client
clean:
	@rm -f *.o *.pb.cc *.pb.h $(TARGET)
