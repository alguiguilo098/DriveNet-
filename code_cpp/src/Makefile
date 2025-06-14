compile:
	@protoc -I ../ --cpp_out=./src/utils/grpc ../command.proto
	@protoc -I ../ --grpc_out=./src/utils/grpc --plugin=protoc-gen-grpc=`which grpc_cpp_plugin` ../command.proto
	
run:
	@g++ -std=c++17 \
	src/main.cpp \
	src/utils/grpc/command.pb.cc \
	src/utils/grpc/command.grpc.pb.cc \
	src/utils/drivenet/Drivenet.cpp \
	`pkg-config --cflags --libs grpc++` -lprotobuf -lpthread -o client
clean:
	@rm -f *.o *.pb.cc *.pb.h $(TARGET)
