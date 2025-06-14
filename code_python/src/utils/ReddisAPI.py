import redis
class RedisAPI:
    def __init__(self,host="localhost",port=6379,db=0,password=None):
        self.__redis= redis.Redis(
            host=host,
            port=port,
            db=db,
            password=password,
            decode_responses=True
        )
    def set(self,key:str,value:dict):
        try:
            if not self.redis.ping():
                raise ConnectionError("Redis server is not reachable")
            self.__redis.set(key,value)
        except redis.ConnectionError as e:
            print(f"Connection error:{e}")
    def get(self,key:str):
        try:
            if not self.redis.ping():
                raise ConnectionError("Redis server is not reachable")
            return self.__redis.get(key)
        except redis.ConnectionError as e:
            print(f"Connection error:{e}")
            return None