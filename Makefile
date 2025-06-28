compile:
	@protoc -I . --cpp_out=./code_cpp/utils/grpc ./command.proto
	@protoc -I . --grpc_out=./code_cpp/utils/grpc --plugin=protoc-gen-grpc=`which grpc_cpp_plugin` ./command.proto
	@python3 -m grpc_tools.protoc -I . --python_out=./code_python --grpc_python_out=./code_python ./command.proto


run:
	@g++ -std=c++17 code_cpp/Main.cpp \
	    code_cpp/utils/grpc/command.pb.cc \
	    code_cpp/utils/grpc/command.grpc.pb.cc \
	    code_cpp/utils/drivenet/Drivenet.cpp \
		code_cpp/utils/base64/base64.cpp\
	    `pkg-config --cflags --libs grpc++` -lprotobuf -lpthread -o client

clean:
	@rm -f code_cpp/utils/grpc/*.pb.cc code_cpp/utils/grpc/*.pb.h client
	@rm -f code_python/command_pb2.py code_python/command_pb2_grpc.py
