from utils.DrivenetAPI import DrivenetAPI
from utils.MongDBAPI import MongoDBAPI
from utils.ReddisAPI import RedisAPI

driveapi=DrivenetAPI(path="google_credencias.json",root_id="1O6auuYW7oJRzE9x0wISjAKBmwsqzoYUO")
mongoapi=MongoDBAPI(url="mongodb://localhost:27017/")
redisapi=RedisAPI(host="localhost",port=6379,db=0,password=None)

def main():
    log=mongoapi.insert_log({
        "timestamp": "2023-10-01T12:00:00Z",
        "mensagem": "Servidor iniciado com sucesso",
        "status": "sucesso"
    })

    log=mongoapi.insert_log({
        "timestamp": "2023-10-01T12:00:00Z",
        "mensagem": "Servidor iniciado com sucesso 1",
        "status": "sucesso"
    })

    log=mongoapi.insert_log({
        "timestamp": "2023-10-01T12:00:00Z",
        "mensagem": "Servidor iniciado com sucesso 3",
        "status": "sucesso"
    })
    
    getlogs=mongoapi.getlogs(limit=3)

    print("Logs:", getlogs)


if __name__=="__main__":
    main()