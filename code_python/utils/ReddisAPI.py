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
    def __decode_base64_to_file(self,base64_string, output_file_path):
        """Decodes a Base64 string back to a file."""
        try:
            decoded_data = base64.b64decode(base64_string)
            with open(output_file_path, 'wb') as file:
                file.write(decoded_data)
            return f"File successfully decoded and saved to: {output_file_path}"
        except Exception as e:
            return f"An error occurred during decoding: {e}"
        
    def set_file(self,id,filepath):
        try:
            if not self.redis.ping():
                raise ConnectionError("Redis server is not reachable")
            if self.__len_size>self.__num_file_size:
                base=self.__encode_file_to_base64(file_path=filepath)
                self.__redis.set(id,base)
                self.__num_file_size+=1
            else:
                self.__redis.delete(id)
                self.__num_file_size-=1
        except redis.ConnectionError as e:
            print(f"Connection error:{e}")
    def get_file(self,key:str):
        try:
            if not self.redis.ping():
                raise ConnectionError("Redis server is not reachable")
            return self.__decode_base64_to_file(self.__redis.get(key),)
        except redis.ConnectionError as e:
            print(f"Connection error:{e}")
            return None