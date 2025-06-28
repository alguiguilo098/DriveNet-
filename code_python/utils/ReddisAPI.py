# RedisAPI.py
# Autor: Guilherme Almeida Lopes
# Data de criação: 28/06/2025
# Descrição: Classe para gerenciar armazenamento temporário de arquivos codificados em base64 no Redis,
# com controle de limite e remoção automática FIFO (First In, First Out).

import base64  # Usado para codificação e decodificação base64 (caso necessário futuramente)
import redis   # Biblioteca para interação com Redis

class RedisAPI:
    def __init__(self, host="localhost", port=6379, db=0, password=None, len_size=5):
        """
        Inicializa a conexão com o Redis e configura o limite de armazenamento.

        Args:
            host (str): Endereço do servidor Redis.
            port (int): Porta do Redis.
            db (int): Índice do banco de dados Redis.
            password (str|None): Senha para autenticação, se necessário.
            len_size (int): Quantidade máxima de arquivos permitidos.
        """
        self.__redis = redis.Redis(
            host=host,
            port=port,
            db=db,
            password=password,
            decode_responses=True  # Garante que os dados retornem como string (e não bytes)
        )
        self.__len_size = len_size
        self.__file_order_list = "file_order_list"  # Lista que mantém ordem de inserção dos arquivos (FIFO)

    def set_file(self, id, base) -> bool:
        """
        Armazena um arquivo (em base64) no Redis, respeitando o limite configurado.

        Args:
            id (str): Chave única para o arquivo.
            base (str): Conteúdo do arquivo em base64.

        Returns:
            bool: True se o arquivo foi salvo com sucesso, False em caso de erro.
        """
        try:
            if not self.__redis.ping():
                raise ConnectionError("Redis server is not reachable")

            # Verifica o número atual de arquivos armazenados
            current_count = self.__redis.llen(self.__file_order_list)

            if current_count >= self.__len_size:
                # Remove o arquivo mais antigo (FIFO)
                oldest_id = self.__redis.lpop(self.__file_order_list)
                if oldest_id:
                    self.__redis.delete(oldest_id)

            if base:
                self.__redis.set(id, base)
                self.__redis.rpush(self.__file_order_list, id)
                return True
            return False

        except redis.ConnectionError as e:
            print(f"Erro de conexão com Redis: {e}")
            return False

    def get_file(self, key: str):
        """
        Recupera o conteúdo de um arquivo salvo no Redis.

        Args:
            key (str): Chave do arquivo a ser recuperado.

        Returns:
            str|None: Conteúdo do arquivo em base64 ou None em caso de falha.
        """
        try:
            if not self.__redis.ping():
                raise ConnectionError("Redis server is not reachable")
            return self.__redis.get(key)
        except redis.ConnectionError as e:
            print(f"Erro de conexão com Redis: {e}")
            return None
