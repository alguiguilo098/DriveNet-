from googleapiclient.discovery import build
from google.oauth2 import service_account

class DrivenetAPI:
    def __init__(self,path:str,root_id:str)->None:
        creds = service_account.Credentials.from_service_account_file(path,scopes=['https://www.googleapis.com/auth/drive'])
        self.__drive_service = build('drive', 'v3', credentials=creds)
        self.__root_id=root_id
    def ls_drivenet(self):
        """Listar arquivos em um diretório do Google Drive
        
        Args: 
            file_id (str): ID do arquivo ou pasta no Google Drive"""
        
        results= self.__drive_service.files().list(
            q=f"'{self.__root_id}' in parents and trashed=false",
            fields="nextPageToken, files(id, name, mimeType, size, modifiedTime)"
        )
        
        return results.execute().get("files",[])
    
    def mkdir_drivenet(self,name):
        """Criar um diretório no Google Drive
        
        Args:
            name (str): Nome do diretório a ser criado
            file_id (str): ID do arquivo ou pasta pai no Google Drive"""
        file_metada={
            'name':name,
            'mimeType':'application/vnd.google-apps.folder',
            'parents':[self.__root_id]
        }
        file=self.__drive_service.files().create(body=file_metada,fields='id')
        return file.execute().get('id')
    
    def rm_drivenet(self,file_id:str)->bool:
        """Remover um arquivo ou diretório do Google Drive
        
        Args:
            file_id (str): ID do arquivo ou pasta a ser removido"""
        
        try:
            self.__drive_service.files().delete(fileId=file_id).execute()
            return True
        except Exception as e:
            return False, str(e)
    
    def cd_drivenet(self,file_id:str)->None:
        """Mudar o diretório atual no Google Drive
        
        Args:
            file_id(str): ID do arquivo ou pasta no Google Drive
        
        """
        self.__root_id= file_id

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
        pass

    def file_download(self,file_path:str)->bool:
        pass
    
