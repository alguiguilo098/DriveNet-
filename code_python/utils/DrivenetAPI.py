import io
from googleapiclient.http import MediaIoBaseDownload, MediaIoBaseUpload
from googleapiclient.discovery import build
from google.oauth2 import service_account 
from utils.MongDBAPI import MongoDBAPI
from utils.ReddisAPI import RedisAPI
from datetime import datetime

class DrivenetAPI:
    def __init__(self,path:str,root_id:str, mongoapi:MongoDBAPI,redisapi:RedisAPI)->None:
        """
        Inicializa a API do Google Drive coma
        """
        creds = service_account.Credentials.from_service_account_file(path,scopes=['https://www.googleapis.com/auth/drive'])
        self.__drive_service = build('drive', 'v3', credentials=creds)
        self.__root_id=root_id
        self.__mongoapi=mongoapi
        self.__redisapi=redisapi 
    def ls_drivenet(self):
        """Listar arquivos em um diretório do Google Drive
        
        Args: 
            file_id (str): ID do arquivo ou pasta no Google Drive
        
        """
        datetime_now= datetime.now() # pega o tempo atual do servidor 
        try:
            results= self.__drive_service.files().list(
                q=f"'{self.__root_id}' in parents and trashed=false",
                fields="nextPageToken, files(id, name, mimeType, size, modifiedTime)"
            ) # lista todas as pastas do diretório atual
            response=results.execute().get("files",[]) # 
            self.__createlogs(datetime_now=datetime_now,mensagem=f"Listar")
            return response
        except Exception as e:
            response=[]
            self.__createlogs(datetime_now=datetime_now,
            mensagem=f"Error ao listar arquivos no diretório {self.__get_name_root()}:{str(e)}",
            status="error")

            return response

    def __createlogs(self, datetime_now,mensagem,status="sucess"):
            self.__mongoapi.insert_log({
                "timestamp": datetime_now.strftime("%d/%m/%Y,%H:%M:%S"),
                "mensagem": mensagem,
                "status": status
            })
    
    def mkdir_drivenet(self,name)->bool:
        """Criar um diretório no Google Drive
        
        Args:
            name (str): Nome do diretório a ser criado
            file_id (str): ID do arquivo ou pasta pai no Google Drive"""
        datetime_now=datetime.now()
        try:
            file_metada={
            'name':name,
            'mimeType':'application/vnd.google-apps.folder',
            'parents':[self.__root_id]
            }
            file=self.__drive_service.files().create(body=file_metada,fields='id')
            response=file.execute().get('id')
            self.__createlogs(datetime_now=datetime_now,
            mensagem=f"Diretório {name} criado com sucesso",
            status="sucess")
            return response
        except  Exception as e:
            self.__createlogs(datetime_now=datetime_now,
            mensagem=f"Error ao criar diretório {name}",
            status="error")
            return []

    
    def rm_drivenet(self,file_name:str)->bool:
        """Remover um arquivo ou diretório do Google Drive
        
        Args:
            file_id (str): ID do arquivo ou pasta a ser removido"""
        
        datetime_now=datetime.now()
        try:
            results = self.__drive_service.files().list(
            q=f"name='{file_name}' and trashed=false",
            spaces='drive',
            fields="files(id, name)").execute()
            item = results.get('files', [])[0]
            self.__drive_service.files().delete(fileId=item["id"]).execute()
            self.__createlogs(datetime_now=datetime_now,
            mensagem=f"Arquivo {file_name} deletado com sucesso"
            )
            return True
        except Exception as e:
            self.__createlogs(datetime_now=datetime_now,
            mensagem=f"Error ao deletar Arquivo com  {file_name}:{str(e)}",
            status="error"
            )
            return False, str(e)
    
    def cd_drivenet(self, file_name: str) -> bool:
        """
        Muda o diretório atual no Google Drive para a pasta com o nome especificado.

        Args:
            file_name (str): Nome do arquivo ou pasta no Google Drive.

        Returns:
            bool: True se a mudança foi bem-sucedida, False caso contrário.
        """
        try:
            results = self.__drive_service.files().list(
            q=f"name = '{file_name}' and trashed = false",
            spaces='drive',
            fields="files(id, name)",
            pageSize=1
        ).execute()

            files = results.get('files', [])
            if not files:
                return False

            self.__root_id = files[0]['id']
            return True

        except Exception as e:
        # Se desejar logar o erro: print(f"Erro ao mudar diretório: {e}")
            return False

        


    def get_current_directory(self)->dict[str,str]:
        """Obter o ID do diretório atual no Google Drive
        
        Returns:
            str: ID do diretório atual
        """
        return {"id":self.__root_id,
                "name":self.__get_name_root()}
    
    def __get_name_root(self):

        """Obter o nome do diretório raiz no Google Drive

        Returns:
            str: Nome do diretório raiz
        """
        try:
            file=self.__drive_service.files().get(fileId=self.__root_id, fields="name").execute()
            return file.get("name")
        except Exception as error:
            print(f"An error occurred: {error}")
            return None
    
    def close(self)->None:
        """Fechar a conexão com o Google Drive API """
        return self.__drive_service.close()
    
    def file_upload(self,file_path:str,file_name:str|None=None)->bool:
        """
            fazer upload de um arquivo para o Google Drive
        """
        file_metadata={
            "parents":[self.__root_id],
            "name":file_name if file_name else file_path.split("/")[-1]
        }
        media= MediaIoBaseUpload(io.FileIO(file_path,"rb"), mimetype="application/octet-stream")
        request= self.__drive_service.files().create(
            body=file_metadata,
            media_body=media,
            fields="id"
        )
        try:
            datetime_now=datetime.now()
            response = request.execute()
            self.__createlogs(datetime_now=datetime_now,
            mensagem=f"Upload do arquivo {file_name} feito com sucesso",
            status="sucess")
            return True, response.get("id")
        except Exception as e:
            self.__createlogs(datetime_now=datetime_now,
            mensagem=f"Erro ao Realizar Upload do Arquivo {file_name}:{str(e)}",
            status="error")
            return False, str(e)

    def file_download(self,file_path:str,file_id)->bool:
        datetime_now=datetime.now()
        try:
            request = self.__drive_service.files().get_media(fileId=file_id)
            fh = io.FileIO(file_path, mode='wb')
    
            downloader = MediaIoBaseDownload(fh, request)
    
            done = False
            while not done:
                _, done = downloader.next_chunk()
            
            self.__createlogs(datetime_now=datetime_now,
            mensagem=f"Dowload do arquivo {file_path} realizado com sucesso")
            return True
        except Exception as e:
            self.__createlogs(datetime_now=datetime_now,
            mensagem=f"Erro ao  realizar Dowload do arquivo {file_path}")
            return True

if __name__=="__main__":
    teste=DrivenetAPI(path="../google_credencias.json",root_id="1S-PQtGE6q6J5jiPC9RLPJaIfj3hE57kn",mongoapi=MongoDBAPI(),redisapi=RedisAPI())
    teste.rm_drivenet("calvoteste")

