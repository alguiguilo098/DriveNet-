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
    def ExecutarComando(self, request, context):
        try:

            if request.comando == "mkdir":
                response=self.__drivenet_auth.mkdir_drivenet(request.argumentos[0])
                responsecommand = command_pb2.ComandoResponse()
                if response!=[]:
                    responsecommand.saida.append(f"Diretório '{request.argumentos[0]}' criado com sucesso.")
                    responsecommand.codigo_saida=1
                else:
                    responsecommand.saida.append(f"Erro ao criar diretório {request.argumentos[0]}")
                    responsecommand.codigo_saida=-1
                return responsecommand
            elif request.comando =="cdnet":
                response=self.__drivenet_auth.cd_drivenet(request.argumentos[0])
                responsecommand = command_pb2.ComandoResponse()
                if response:
                    responsecommand.saida.append(f" Mudança para o Diretório '{request.argumentos[0]}'sucesso.")
                    responsecommand.codigo_saida=4
                else:
                    responsecommand.saida.append(f"Erro ao mudar Diretório {request.argumentos[0]}")
                    responsecommand.codigo_saida=-4
                return responsecommand
            elif request.comando =="rmnet":
                response=self.__drivenet_auth.rm_drivenet(request.argumentos[0])
                responsecommand=command_pb2.ComandoResponse()
                if response: 
                    responsecommand.saida.append(f"Arquivo removido {responsecommand.argumentos[0]} com sucesso")
                    responsecommand.codigo_saida=3
                elif not response:
                    responsecommand.saida.append(f"Erro ao remover Arquivo {responsecommand.argumentos[0]}")
                    responsecommand.codigo_saida=-3
                return responsecommand
            elif request.comando =="upnet":
                result = self.__drivenet_auth.file_upload(
                file_name=request.argumentos[0],
                base=request.argumentos[1]
                )

                responsecommand = command_pb2.ComandoResponse()

                if result[0]:
                    responsecommand.saida.append(f"Upload do arquivo {request.argumentos[0]} com sucesso")
                    responsecommand.codigo_saida = 5
                else:
                    responsecommand.saida.append(f"Erro ao realizar Upload do arquivo {request.argumentos[0]}: {result[1]}")
                    responsecommand.codigo_saida = -5
                    print(result[1])
                return responsecommand
            elif request.comando =="downet":
                base64filearquivo=self.__drivenet_auth.file_download(request.argumentos[0])
                responsecommand=command_pb2.ComandoResponse()
                if base64filearquivo!=None:
                    responsecommand.saida.append(base64filearquivo)
                    responsecommand.codigo_saida=6
                else:
                    responsecommand.saida.append(f"Erro ao realizar Dowload do arquivo {request.argumentos[0]}")
                    responsecommand.codigo_saida=-6
                return responsecommand
            elif request.comando == "drivenet":
                pass
            elif request.comando == "lsnet":
                response=self.__drivenet_auth.ls_drivenet()
                responsecommand = command_pb2.ComandoResponse()
                if response!=[]:
                    for i in response:
                        responsecommand.saida.append(f"{i['id']},{i['name']},{i.get("size","N/A")},{i['mimeType']},{i['modifiedTime']}")
                    responsecommand.codigo_saida=2
                    return responsecommand
                else:
                    responsecommand.saida.append("Erro ao listar diretório")
                    responsecommand.codigo_saida=-2
                    return responsecommand
                
            elif request.comando == "lastlog":
                requestlogs = mongoapi.getlogs(int(request.argumentos[0]))
                responsecommand = command_pb2.ComandoResponse()
                for i in requestlogs:
                    responsecommand.saida.append(f"{i['timestamp']} {i['mensagem']} status: {i['status']}")
                lastlog=mongoapi.getlogs(1)[0]
                print(f"{lastlog['timestamp']} status: {lastlog['status']} {lastlog['mensagem']}")
                return responsecommand
            
            else:            
                # Resposta padrão (caso nada seja tratado acima)
                response = command_pb2.ComandoResponse()
                response.saida.append("Comando não reconhecido")
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
