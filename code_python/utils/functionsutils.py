import base64
import json
import hashlib 

def save_json_base64(base64_str, caminho_saida_json):
    """
    Decodifica uma string Base64 contendo um JSON e salva como arquivo .json.

    Args:
        base64_str (str): A string Base64 representando um conteúdo JSON.
        caminho_saida_json (str): Caminho completo para salvar o arquivo .json.
    """
    try:
        # Remove prefixo se houver (como data:application/json;base64,...)
        if base64_str.startswith("data:"):
            base64_str = base64_str.split(",", 1)[1]
        
        # Decodifica a string Base64 para bytes
        json_bytes = base64.b64decode(base64_str)
        
        # Converte os bytes em string
        json_str = json_bytes.decode("utf-8")
        
        # Valida o conteúdo como JSON
        json_obj = json.loads(json_str)
        
        # Salva no arquivo de saída
        with open(caminho_saida_json, "w", encoding="utf-8") as f:
            json.dump(json_obj, f, ensure_ascii=False, indent=4)

        return caminho_saida_json
    
        
    except Exception as e:
        print(f"Erro ao salvar o JSON: {e}")

def calculate_sha256(file_path, chunk_size=8192):
    """
    Calculates the SHA256 hash of a given file.

    Args:
        file_path (str): The path to the file.
        chunk_size (int): The size of chunks to read the file in bytes.
                          Defaults to 8192 bytes.

    Returns:
        str: The hexadecimal representation of the SHA256 hash, or None if the file is not found.
    """
    sha256_hash = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                sha256_hash.update(chunk)
        return sha256_hash.hexdigest()
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return None