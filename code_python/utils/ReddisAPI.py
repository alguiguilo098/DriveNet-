import base64  # Usado para codificar o arquivo em base64
import redis    # Biblioteca cliente para interação com o servidor Redis

class RedisAPI:
    def __init__(self, host="localhost", port=6379, db=0, password=None, len_size=5):
        # Inicializa conexão com o Redis
        self.__redis = redis.Redis(
            host=host,
            port=port,
            db=db,
            password=password,
            decode_responses=True  # Decodifica os dados retornados como string
        )
        self.__num_file_size = 0     # Contador de arquivos atualmente salvos no Redis
        self.__len_size = len_size   # Número máximo de arquivos que podem ser salvos
        self.__len_size = len_size
        self.__file_order_list = "file_order_list"  # Lista Redis para rastrear ordem dos arquivos

    def set_file(self, id, base):
        """
        Salva um arquivo (base64) no Redis. Remove o mais antigo se o limite for atingido.
        """
        try:
            if not self.__redis.ping():
                raise ConnectionError("Redis server is not reachable")

            # Verifica quantidade atual
            current_count = self.__redis.llen(self.__file_order_list)

            if current_count >= self.__len_size:
                # Remove o arquivo mais antigo
                oldest_id = self.__redis.lpop(self.__file_order_list)  # Remove da lista
                if oldest_id:
                    self.__redis.delete(oldest_id)  # Remove do Redis

            if base:
                self.__redis.set(id, base)  # Armazena o arquivo
                self.__redis.rpush(self.__file_order_list, id)  # Adiciona o ID ao final da lista (ordem FIFO)
                return True
            return False

        except redis.ConnectionError as e:
            print(f"Connection error: {e}")
            return False
    def get_file(self, key: str):
        """
        Recupera o conteúdo (base64) de um arquivo salvo no Redis pela chave
        """
        try:
            if not self.__redis.ping():  # Verifica a conexão com o Redis
                raise ConnectionError("Redis server is not reachable")
            return self.__redis.get(key)  # Retorna o conteúdo da chave
        except redis.ConnectionError as e:
            print(f"Connection error: {e}")
            return None
