from utils.DrivenetAPI import DrivenetAPI
from utils.MongDBAPI import MongoDBAPI
from utils.ReddisAPI import RedisAPI

driveapi=DrivenetAPI(path="google_credencias.json",root_id="1S-PQtGE6q6J5jiPC9RLPJaIfj3hE57kn")
mongoapi=MongoDBAPI(url="mongodb://localhost:27017/")
redisapi=RedisAPI(host="localhost",port=6379,db=0,password=None)

def main():
    print(driveapi.ls_drivenet())
    driveapi.file_download(file_id="1Bmr5Lpk-xMh3QEtql1U1LtweXEcCjalz",file_path="teste.pdf")
    driveapi.file_upload(file_path="./teste.pdf",file_name="teste200.pdf")


if __name__=="__main__":
    main()