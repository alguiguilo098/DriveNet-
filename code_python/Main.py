from dotenv import load_dotenv
import os
from grpc_reflection.v1alpha import reflection
from utils.MongDBAPI import MongoDBAPI
from utils.DrivenetAPI import DrivenetAPI 
from utils.ReddisAPI import RedisAPI
import grpc
from concurrent import futures
import time
import command_pb2_grpc
import command_pb2 

# Load environment variables from .env file
load_dotenv()

urlmongo = os.getenv("MONGO_DB_HOST")
port = os.getenv("REDIS_PORT")
host = os.getenv("REDIS_HOST")

mongoapi = MongoDBAPI(url=urlmongo)
reddis = RedisAPI(host=host, port=port)

class DriveNetServer(command_pb2_grpc.TerminalServiceServicer):
    def __init__(self):
        super().__init__()
        self.__drivenet_auth=DrivenetAPI(path="google_credencias.json",root_id="1S-PQtGE6q6J5jiPC9RLPJaIfj3hE57kn",mongoapi=mongoapi,redisapi=reddis)
        print("Server")
    def ExecutarComando(self, request, context):
        print("Server Executado")
        try:
            if request.comando == "drivenet" and len(request.argumentos) >= 2:
                pass               
            elif request.comando == "lastlog":
                print(request.comando)
                requestlogs = mongoapi.getlogs(int(request.argumentos[0]))
                print(requestlogs)
                print("Teste ")
                responsecommand = command_pb2.ComandoResponse()
                for i in requestlogs:
                    responsecommand.saida.append(f"{i['timestamp']} status: {i['status']} {i['mensagem']}")
                return responsecommand
            else:            
                # Resposta padrão (caso nada seja tratado acima)
                response = command_pb2.ComandoResponse()
                response.saida.append("Comando não reconhecido ou sem implementação.")
                return response

        except Exception as e:
            response = command_pb2.ComandoResponse()
            response.saida.append(f"Erro ao executar comando: {str(e)}")
            return response


def server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    command_pb2_grpc.add_TerminalServiceServicer_to_server(DriveNetServer(), server)

    SERVICE_NAMES = (
        command_pb2.DESCRIPTOR.services_by_name['TerminalService'].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(SERVICE_NAMES, server)

    # Porta padrão
    grpc_port = os.getenv("GRPC_PORT", "50051")
    server.add_insecure_port(f'[::]:{grpc_port}')
    print(f"gRPC Server iniciado na porta {grpc_port}")
    server.start()

    try:
        while True:
            time.sleep(86400)  # Mantém o servidor vivo por 1 dia
    except KeyboardInterrupt:
        print("Encerrando servidor...")
        server.stop(0)


if __name__ == "__main__":
    server()
