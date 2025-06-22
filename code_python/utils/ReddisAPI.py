import base64
import redis
class RedisAPI:
    def __init__(self,host="localhost",port=6379,db=0,password=None,len_size=5):
        self.__redis= redis.Redis(
            host=host,
            port=port,
            db=db,
            password=password,
            decode_responses=True
        )
        self.__num_file_size=0
        self.__len_size=len_size
        
    def __encode_file_to_base64(self,file_path):
        try:
            with open(file_path, "rb") as file:
                file_content = file.read()
                encoded_string = base64.b64encode(file_content).decode('utf-8')
            return encoded_string
        except FileNotFoundError:
            print(f"Erro: Arquivo não encontrado em {file_path}")
            return None
        except Exception as e:
            print(f"Erro ao codificar o arquivo: {e}")
        
    def set_file(self,id,filepath):
        try:
            if not self.__redis.ping():
                raise ConnectionError("Redis server is not reachable")
            if self.__len_size>self.__num_file_size:
                base=self.__encode_file_to_base64(file_path=filepath)
                self.__redis.set(id,base)
                self.__num_file_size+=1
            else:
                self.deltekey(id)
        except redis.ConnectionError as e:
            print(f"Connection error:{e}")

    def new_method(self, id):
        self.__redis.delete(id)
        self.__num_file_size-=1
    def get_file(self,key:str):
        try:
            if not self.__redis.ping():
                raise ConnectionError("Redis server is not reachable")
            return self.__redis.get(key)
        except redis.ConnectionError as e:
            print(f"Connection error:{e}")
            return None