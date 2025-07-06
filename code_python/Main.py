from dotenv import load_dotenv
import os
from grpc_reflection.v1alpha import reflection
from utils.MongDBAPI import MongoDBAPI
from utils.DrivenetAPI import DrivenetAPI 
from utils.ReddisAPI import RedisAPI
import grpc
from utils.functionsutils import save_json_base64,calculate_sha256
from concurrent import futures
import time
import command_pb2_grpc
import command_pb2 
import uuid
# Load environment variables from .env file
load_dotenv()

urlmongo = os.getenv("MONGO_DB_HOST")
port = os.getenv("REDIS_PORT")
host = os.getenv("REDIS_HOST")


mongoapi = MongoDBAPI(url=urlmongo)
reddis = RedisAPI(host=host, port=port)

class DriveNetServer(command_pb2_grpc.TerminalServiceServicer):
    def __init__(self):
        self.__conections={}
    def ExecutarComando(self, request, context):
        try:
            if request.comando == "drivenet":
                random_name = str(uuid.uuid4()) # Gera u
                path_file=save_json_base64(request.argumentos[1],f"credencias_json/{random_name}.json")
                hash=calculate_sha256(path_file)
                self.__conections[hash]=DrivenetAPI(path=path_file,root_id=request.argumentos[0],mongoapi=mongoapi,redisapi=reddis,hash=hash)
                responsecommand = command_pb2.ComandoResponse()
                responsecommand.saida.append(f"{hash},{random_name}")
                return responsecommand
            
            elif request.comando == "mkdirnet":
                response=self.__conections[request.hash_cliente].mkdir_drivenet(request.argumentos[0])
                responsecommand = command_pb2.ComandoResponse()
                if response!=[]:
                    responsecommand.saida.append(f"Diretório '{request.argumentos[0]}' criado com sucesso.")
                    responsecommand.codigo_saida=1
                else:
                    responsecommand.saida.append(f"Erro ao criar diretório {request.argumentos[0]}")
                    responsecommand.codigo_saida=-1
                self.lastlog(request.hash_cliente)
                return responsecommand
            elif request.comando =="cdnet":
                response=self.__conections[request.hash_cliente].cd_drivenet(request.argumentos[0])
                responsecommand = command_pb2.ComandoResponse()
                if response:
                    responsecommand.saida.append(f" Mudança para o Diretório '{request.argumentos[0]}'sucesso.")
                    responsecommand.codigo_saida=4
                else:
                    responsecommand.saida.append(f"Erro ao mudar Diretório {request.argumentos[0]}")
                    responsecommand.codigo_saida=-4
                self.lastlog(request.hash_cliente)
                return responsecommand
            elif request.comando =="rmnet":
                response=self.__conections[request.hash_cliente].rm_drivenet(request.argumentos[0])
                responsecommand=command_pb2.ComandoResponse()
                if response: 
                    responsecommand.saida.append(f"Arquivo removido {request.argumentos[0]} com sucesso")
                    responsecommand.codigo_saida=3
                elif not response:
                    responsecommand.saida.append(f"Arquivo {request.argumentos[0]} não encontrado")
                    responsecommand.codigo_saida=-3
                self.lastlog(request.hash_cliente)
                return responsecommand
            elif request.comando =="upnet":
                result = self.__conections[request.hash_cliente].file_upload(
                file_name=request.argumentos[1],
                base=request.argumentos[0]
                )
                responsecommand = command_pb2.ComandoResponse()
                if result[0]:
                    responsecommand.saida.append(f"Upload do arquivo {request.argumentos[0]} com sucesso")
                    responsecommand.codigo_saida = 5
                else:
                    responsecommand.saida.append(f"Erro ao realizar Upload do arquivo {request.argumentos[0]}: {result[1]}")
                    responsecommand.codigo_saida = -5
                self.lastlog(request.hash_cliente)
                return responsecommand
            elif request.comando =="downet":

                base64filearquivo=self.__conections[request.hash_cliente].file_download(request.argumentos[0])
                responsecommand=command_pb2.ComandoResponse()
                if base64filearquivo!=None:
                    responsecommand.saida.append(base64filearquivo)
                    responsecommand.codigo_saida=6
                else:
                    responsecommand.saida.append(f"Erro ao realizar Dowload do arquivo {request.argumentos[0]}")
                    responsecommand.codigo_saida=-6
                self.lastlog(request.hash_cliente)
                return responsecommand
            elif request.comando == "lsnet":
                response=self.__conections[request.hash_cliente].ls_drivenet()
                responsecommand = command_pb2.ComandoResponse()
                if response!=[]:
                    for i in response:
                        responsecommand.saida.append(f"{i['id']},{i['name']},{i.get("size","N/A")},{i['mimeType']},{i['modifiedTime']}")
                    responsecommand.codigo_saida=2
                    self.lastlog(request.hash_cliente)
                    return responsecommand
                else:
                    responsecommand.saida.append("Erro ao listar diretório")
                    responsecommand.codigo_saida=-2
                    self.lastlog(request.hash_cliente)
                    return responsecommand
                
            elif request.comando == "lastlog":
                requestlogs = mongoapi.getlogs(int(request.argumentos[0]),request.hash_cliente)
                responsecommand = command_pb2.ComandoResponse()
                for i in requestlogs:
                    responsecommand.saida.append(f"hash:{i["hash"]} {i['timestamp']} {i['mensagem']} status: {i['status']}")
                self.lastlog(request.hash_cliente)
                return responsecommand
            elif request.comando == "exit":
                print(request)
                responsecommand = command_pb2.ComandoResponse()
                chave = request.hash_cliente
                if chave in self.__conections:
                    self.__conections.pop(chave)

                # Remove o arquivo de credenciais se existir
                caminho_arquivo = f"./credencias_json/{request.argumentos[0]}.json"
                if os.path.exists(caminho_arquivo):
                    os.remove(caminho_arquivo)

                responsecommand.saida.append(f"Conexão {chave} encerrada e credenciais removidas.")
                responsecommand.codigo_saida = 0

                return responsecommand
            else:
                self.lastlog(request.hash_cliente)            
                # Resposta padrão (caso nada seja tratado acima)
                response = command_pb2.ComandoResponse()
                response.saida.append("Comando não reconhecido")
                return response
            
        except Exception as e:
            response = command_pb2.ComandoResponse()
            response.saida.append(f"Erro ao executar comando: {str(e)}")
            return response

    def lastlog(self,hash):
        lastlog=mongoapi.getlogs(1,hash=hash)[0]
        print(f"{lastlog['timestamp']} {lastlog['hash']} status: {lastlog['status']} {lastlog['mensagem']}")


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
