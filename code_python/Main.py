from dotenv import load_dotenv
import os
from utils.MongDBAPI import MongoDBAPI
from utils.DrivenetAPI import DrivenetAPI 
from utils.ReddisAPI import RedisAPI
import grpc
from concurrent import futures
import time
import utils.command_pb2_grpc
import utils.command_pb2 

# Load environment variables from .env file
load_dotenv()

os.getenv("MONGO_DB_HOST")
port=os.getenv("REDIS_PORT")
host=os.getenv("REDIS_HOST")
def decode_base64_in_json():
   pass

class DriveNetServer(utils.command_pb2_grpc.TerminalServiceServicer):
   def __init__(self):
      super().__init__()
      self.__drivenet_auth={}
    
   def ExecutarComando(self, request, context):
      try:
        if request.commando=="drivenet" and True :
            pass 
        if request.comando=="lsnet" and True:
            pass
        elif request.comando=="cdnet" and True:
            pass
        elif request.comando=="mkdirnet" and True:
            pass
        elif request.comando=="upnet" and True:
            pass
        elif request.comando=="downet" and True:
            pass
        elif request.comando=="pwdnet" and True:
            pass
        elif request.comando=="rmnet" and True:
            pass
        elif request.comando=="chmodnet" and True:
            pass
        elif request.comando=="lastlog" and True:
            pass
      except Exception as e:
         pass
      
def server():
    pass

if __name__=="__main__":
    pass