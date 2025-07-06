import base64
import io
from googleapiclient.http import MediaIoBaseDownload, MediaIoBaseUpload
from googleapiclient.discovery import build
from google.oauth2 import service_account 
from utils.MongDBAPI import MongoDBAPI
from utils.ReddisAPI import RedisAPI
from datetime import datetime

def safe_base64_decode(data: str) -> bytes:
    # Remove quebras de linha e espaços
    data = data.strip().replace("\n", "").replace("\r", "")

    # Adiciona '=' se necessário para múltiplos de 4
    missing_padding = len(data) % 4
    if missing_padding:
        data += '=' * (4 - missing_padding)

    return base64.b64decode(data)

"""
  Descricao:DrivenetAPI fornece uma interface de alto nível para interagir com o Google Drive, 
  utilizando autenticação via credenciais de serviço e integração com MongoDB para logs e Redis para cache de arquivos.
"""
class DrivenetAPI:
    def __init__(self,path:str,root_id:str, mongoapi:MongoDBAPI,redisapi:RedisAPI)->None:
        """
        Inicializa a API do Google Drive coma
        """
        creds = service_account.Credentials.from_service_account_file(path,scopes=['https://www.googleapis.com/auth/drive'])
        self.__drive_service = build('drive', 'v3', credentials=creds)
        self.__root_id=root_id # id do diretório root
        self.__mongoapi=mongoapi # API MongoDB
        self.__redisapi=redisapi # API Redis
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
            ) # realizando a query
            response=results.execute().get("files",[]) # pegangos os json com dados dos arquivo e diretórios
            self.__createlogs(datetime_now=datetime_now,mensagem=f"Sucesso ao Lista diretórios",status="sucess") 
            return response
        except Exception as e:
            response=[]# retorna uma lista vazia
            self.__createlogs(datetime_now=datetime_now,
            mensagem=f"Error ao listar arquivos no diretório {self.__get_name_root()}:{str(e)}", 
            status="error") # cria log no mongoDB

            return response

    def __createlogs(self, datetime_now,mensagem,status="sucess"):
            self.__mongoapi.insert_log({
                "timestamp": datetime_now.strftime("%d/%m/%Y,%H:%M:%S"), # quando a operação no servidor foi realizado
                "mensagem": mensagem, # descrição do evento
                "status": status # status (sucess, error)
            })
    
    def mkdir_drivenet(self,name)->bool:
        """Criar um diretório no Google Drive
        
        Args:
            name (str): Nome do diretório a ser criado
            file_id (str): ID do arquivo ou pasta pai no Google Drive"""
        datetime_now=datetime.now()  # data atual do server
        try:
            file_metada={
            'name':name, # nome
            'mimeType':'application/vnd.google-apps.folder', # tipo do arquivo(diretório)
            'parents':[self.__root_id] # diretório onde vai ser criado o diretório
            }
            file=self.__drive_service.files().create(body=file_metada,fields='id') # cria o diretório 
            response=file.execute().get('id') # pega o id 
            self.__createlogs(datetime_now=datetime_now,
            mensagem=f"Diretório {name} criado com sucesso",
            status="sucess") # cria o log da operação no mongo DB
            return response
        except  Exception as e:
            # retorna um lista vazia , quando a operação falha
            self.__createlogs(datetime_now=datetime_now,
            mensagem=f"Error ao criar diretório {name}",
            status="error") # gera log de erro
            return [] 

    
    def rm_drivenet(self,file_name:str)->bool:
        """Remover um arquivo ou diretório do Google Drive
        
        Args:
            file_id (str): ID do arquivo ou pasta a ser removido"""
        
        datetime_now=datetime.now() # data atual do servidor
        try:
            results = self.__drive_service.files().list(
            q=f"name='{file_name}' and trashed=false",
            spaces='drive',
            fields="files(id, name)").execute() # busca o id do arquivo
            item = results.get('files', []) # pega o primeiro arquivo obtido
            if len(item) == 0:
                self.__createlogs(datetime_now=datetime_now,
                mensagem=f"Arquivo {file_name} não encontrado no Google Drive.",
                status="error"
                )
                return False
            self.__drive_service.files().delete(fileId=item[0]["id"]).execute() # remove arquivo
            self.__createlogs(datetime_now=datetime_now,
            mensagem=f"Arquivo {file_name} deletado com sucesso"
            ) # gera o log no monogo DB
            return True
        except Exception as e:
            # gera o log de erro da operação remover
            self.__createlogs(datetime_now=datetime_now,
            mensagem=f"Error ao deletar Arquivo com  {file_name}:{str(e)}",
            status="error"
            )
            return False, str(e) # retorna para usuário o erro, e falha da operação
    

    def cd_drivenet(self, file_name: str) -> bool:
        """
        Muda o diretório atual no Google Drive para a pasta com o nome especificado,
        ou volta um nível se for '..'.

        Args:
            file_name (str): Nome da pasta (ou '..' para voltar).

        Returns:
            bool: True se a mudança foi bem-sucedida, False caso contrário.
        """
        datetime_now = datetime.now()
        try:
            # Voltar para o diretório pai
            if file_name == "..":
                if not self.__root_id:
                    return False  # Diretório atual indefinido

                metadata = self.__drive_service.files().get(
                fileId=self.__root_id,
                fields="parents"
                ).execute()

                parents = metadata.get("parents", [])
                if not parents:
                    return False  # Já está no root

                self.__root_id = parents[0]
                self.__createlogs(
                datetime_now=datetime_now,
                mensagem="Diretório alterado para o diretório pai (..)"
                )
                return True
                return True

            # Entrar na pasta filha com nome específico
            results = self.__drive_service.files().list(
                q=(
                    f"name = '{file_name}' "
                    f"and '{self.__root_id}' in parents "
                    "and mimeType = 'application/vnd.google-apps.folder' "
                    "and trashed = false"
                ),
                spaces='drive',
                fields="files(id, name)",
                pageSize=1
            ).execute()

            files = results.get('files', [])
            if not files:
                return False

            self.__root_id = files[0]['id']
            self.__createlogs(
                datetime_now=datetime_now,
                mensagem=f"Diretório alterado para '{file_name}'"
            )
            return True

        except Exception as e:
            self.__createlogs(
            datetime_now=datetime_now,
            mensagem=f"[ERRO] Falha ao mudar diretório: {str(e)}",
            status="error"
            )
        return False

        


    def get_current_directory(self)->dict[str,str]:
        """Obter o ID do diretório atual no Google Drive
        
        Returns:
            str: ID do diretório atual
        """
        # retorna o id e nome do diretório atual
        return {"id":self.__root_id,
                "name":self.__get_name_root()}
    
    def __get_name_root(self):

        """Obter o nome do diretório raiz no Google Drive

        Returns:
            str: Nome do diretório raiz
        """
        try:
            file=self.__drive_service.files().get(fileId=self.__root_id, fields="name").execute()
            return file.get("name") # nome do diretório
        except Exception as error:
            print(f"An error occurred: {error}")
            return None
    
    def close(self)->None:
        """Fechar a conexão com o Google Drive API """
        return self.__drive_service.close() # fecha a conexão com google drive
    
    def file_upload(self,base:str,file_name:str)->bool:
        """
            fazer upload de um arquivo para o Google Drive
        """
        # Decodifica base64 em bytes e cria stream para upload
        datetime_now=datetime.now()
        try:
            file_bytes = safe_base64_decode(base)
            file_stream = io.BytesIO(file_bytes)

            file_metadata={
            "parents":[self.__root_id],
            "name":file_name 
            }
            media= MediaIoBaseUpload(file_stream, mimetype="application/octet-stream")
            #cria o arquivo no google drive com base dados e metadados
            request= self.__drive_service.files().create(
                body=file_metadata,
                media_body=media,
                fields="id"
            )

            response = request.execute() # executa o requisição

            file_id = response.get("id") # pega o id do arquivo
            self.__redisapi.set_file(file_id,base) # coloca o arquivo em base64, no reddis

            self.__createlogs(datetime_now=datetime_now,
            mensagem=f"Upload do arquivo {file_name} feito com sucesso",
            status="success") 
            return True, file_id # retorna o id do arquivo
        except Exception as e:
            self.__createlogs(datetime_now=datetime_now,
            mensagem=f"Erro ao Realizar Upload do Arquivo {file_name}:{str(e)}",
            status="error") # gera o log de erro
            return False, str(e)

    def file_download(self, file_name: str) -> str | None:
        datetime_now = datetime.now()

        try:
            result = self.__drive_service.files().list(
            q=f"name='{file_name}' and trashed=false and '{self.__root_id}' in parents",
            spaces='drive',
            fields="files(id)",
            pageSize=1
            ).execute()

            files = result.get("files", [])
            if not files:
                self.__createlogs(
                datetime_now=datetime_now,
                mensagem=f"Arquivo {file_name} não encontrado no Google Drive.",
                status="error"
                )
                return None

            file_id = files[0]["id"]

             # Tenta obter do Redis
            cached = self.__redisapi.get_file(file_id)
            if cached:
                self.__createlogs(
                datetime_now=datetime_now,
                mensagem=f"Download do arquivo {file_name} realizado com sucesso (Redis)",
                status="success"
            )
                return cached
            
            # Faz download do Google Drive
            request = self.__drive_service.files().get_media(fileId=file_id)
            fh = io.BytesIO()
            downloader = MediaIoBaseDownload(fh, request)

            done = False
            while not done:
                _, done = downloader.next_chunk()

            fh.seek(0)
            encoded_base64 = base64.b64encode(fh.read()).decode("utf-8")

            # Armazena no Redis para cache futuro
            self.__redisapi.set_file(file_id, encoded_base64)

            # Log de sucesso
            self.__createlogs(
                datetime_now=datetime_now,
                mensagem=f"Download do arquivo {file_name} realizado com sucesso (Drive)",
                status="success"
            )
            return encoded_base64

        except Exception as e:
            self.__createlogs(
            datetime_now=datetime_now,
            mensagem=f"Erro ao realizar download do arquivo {file_name}: {e}",
            status="error"
            )
            return None
