import pymongo

class MongoDBAPI:
    def __init__(self,url="mongodb://localhost:27017/"):
        self.__client=pymongo.MongoClient(url)
        self.__dblogs=self.__client["logger"]
        self.__dirs_acess=self.__client["dirs_acess"]
    
    def insert_log(self,log:dict)->bool:
        """Inserir um log no banco de dados MongoDB
        
        Args:
            log(dict): Dicionário contendo o log a ser inserido"""
        try:
            self.__dblogs["logs"].insert_one({
                "timestamp":log.get("timestamp"),
                "mensagem":log.get("mensagem"),
                "status":log.get("status")
            })
            return True
        except Exception as e:
            print(f"Erro ao inserir log: {e}")
            return False
    
    def getlogs(self,limit:int=10)->list[dict]:
        """Obter logs do banco de dados MongoDB
        Args:
            limit(int): Numero máximos de logs a serem retornados 
            
        """

        logs=self.__dblogs["logs"].find().sort("timestamp",-1).limit(limit)
        return list(logs)
    
    def insert_dir_acess(self,dir_acess:dict)->bool:
        """Inserir um diretório acessado no banco de dados MongoDB
        
        Args:
            dir_acess(dict): Dicionário contendo o diretório a ser inserido
        
        """
        try:
            self.__dirs_acess["dirs_acess"].insert_one({
                "dir_root_id": dir_acess.get("dir_id"),
                "dir_name": dir_acess.get("dir_name"),
                "timestamp": dir_acess.get("timestamp"),
            })
            return True
        except Exception as e:
            print(f"Erro ao inserir diretório acessado:{e}")
            return False
    
    def get_dir_acess(self,limit:int=10)->list[dict]:
        """
        Obter diretórios acessados do banco de dados MongoDB
        Args:
            limit(int): Numero máximos de diretórios acessados a serem retornados
        """
        try:
            dirs_acess=self.__dirs_acess["dirs_acess"].find().limit(limit)
            return list(dirs_acess)
        except Exception as e:
            print("Erro ao obter diretórios acessados:",e)
            return []
    def close(self)->None:
        """Fechar a conxão com o MongoDB"""
        self.__client.close()