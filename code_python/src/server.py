from datetime import datetime
from utils.MongDBAPI import MongoDBAPI
from utils.ReddisAPI import RedisAPI


mongoapi=MongoDBAPI()

def main():
    mongoapi.insert_log({
                "timestamp": datetime.now().strftime("%d/%m/%Y, %H:%M:%S"),
                "mensagem": "mensagem1",
                "status": "err"
            })
    print(mongoapi.getlogs(3))
    


if __name__=="__main__":
    main()