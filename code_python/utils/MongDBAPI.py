# MongoDBAPI.py
# Autor: Guilherme Almeida Lopes
# Data de criação: 28/06/2025

# Descrição: Classe para interação com banco de dados MongoDB usando PyMongo, com foco em registro e recuperação de logs.

import pymongo  # Biblioteca para comunicação com o MongoDB

class MongoDBAPI:
    def __init__(self, url="mongodb://127.0.0.1:27017,127.0.0.1:27018,127.0.0.1:27019/?replicaSet=rs0"):
        """
        Inicializa a conexão com o MongoDB, usando um replicaset para alta disponibilidade.
        """
        print(f"Conectando ao MongoDB: {url}")
        self.__client = pymongo.MongoClient(url)           # Cliente MongoDB
        self.__dblogs = self.__client["logger"]            # Banco de dados para armazenar logs
        self.__dirs_acess = self.__client["dirs_acess"]    # Banco de dados para diretórios acessados (reserva para uso futuro)

    def insert_log(self, log: dict) -> bool:
        """
        Insere um log no banco de dados MongoDB.

        Args:
            log (dict): Dicionário com as chaves 'timestamp', 'mensagem' e 'status'.

        Returns:
            bool: True se o log foi inserido com sucesso, False em caso de erro.
        """
        try:
            self.__dblogs["logs"].insert_one({
                "timestamp": log.get("timestamp"),
                "mensagem": log.get("mensagem"),
                "status": log.get("status")
            })
            return True
        except Exception as e:
            print(f"Erro ao inserir log: {e}")
            return False

    def getlogs(self, limit: int = 10) -> list[dict]:
        """
        Recupera os logs mais recentes do MongoDB.

        Args:
            limit (int): Quantidade máxima de logs a retornar. Padrão: 10.

        Returns:
            list[dict]: Lista de logs ordenados por timestamp decrescente.
        """
        logs = self.__dblogs["logs"].find().sort("timestamp", -1).limit(limit)
        return list(logs)  # Converte o cursor em lista de dicionários

    def close(self) -> None:
        """
        Encerra a conexão com o MongoDB.
        """
        self.__client.close()
