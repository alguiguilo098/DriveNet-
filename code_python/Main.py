from dotenv import load_dotenv
import os
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

monogapi = MongoDBAPI(url=urlmongo)
reddis = RedisAPI(host=host, port=port)

class DriveNetServer(command_pb2_grpc.TerminalServiceServicer):
    def __init__(self):
        super().__init__()
        self.__drivenet_auth = {}
        
    def ExecutarComando(self, request, context):
        try:
            if request.comando == "drivenet" and len(request.argumentos) >= 2:
                pass 
            elif request.comando == "lsnet":
                pass
            elif request.comando == "cdnet":
                pass
            elif request.comando == "mkdirnet":
                pass
            elif request.comando == "upnet":
                pass
            elif request.comando == "downet":
                pass
            elif request.comando == "pwdnet":
                pass
            elif request.comando == "rmnet":
                pass
            elif request.comando == "chmodnet":
                pass
            elif request.comando == "lastlog" and len(request.argumentos) > 0:
                requestlogs = monogapi.getlogs(request.argumentos[0])
                responsecommand = utils.command_pb2.ComandoResponse()
                for i in requestlogs:
                    responsecommand.saida.append(f"{i['timestamp']} status: {i['status']} {i['mensagem']}")
                return responsecommand
            else:            
                # Resposta padrão (caso nada seja tratado acima)
                response = utils.command_pb2.ComandoResponse()
                response.saida.append("Comando não reconhecido ou sem implementação.")
                return response

        except Exception as e:
            response = utils.command_pb2.ComandoResponse()
            response.saida.append(f"Erro ao executar comando: {str(e)}")
            return response


def server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    command_pb2_grpc.add_TerminalServiceServicer_to_server(DriveNetServer(), server)
    
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
