import requests

class Spaces():
    """Coleta os dados de todos os espaços
    Args:
        auth (str):{Authorization:token}
        workspace_id (int): id
    """
    def __init__(self,auth:dict,workspace_id:int) -> None:
        self.auth = auth
        self.workspaceID = workspace_id
        self.endpoint = f"https://api.clickup.com/api/v2/team/{self.workspaceID}/space?archived=false"
        self._flag_spaces = 1 # Inicializa o cache para os espaços
        
    def getSpaces(self)->list:
        """Retorna uma lista com todos os espaços do usuário
        """
        
        spaces_json = {} 
        all_spaces = [] # Inicializa para evitar NameError
        spaces_response = requests.get(self.endpoint,headers=self.auth)
        if spaces_response.status_code == 200:
            spaces_json = spaces_response.json()
            all_spaces = spaces_json.get("spaces", [])
            if all_spaces and self._flag_spaces:
                print("Espaços acessados com sucesso:")
                for space_item in all_spaces: # Renomeado para evitar conflito com a classe
                    print(f"- {space_item["name"]}")
            else:
                print("Nenhum espaço encontrado.")
        else:
            print(f"Erro na conexão com a API ao acessar os espaços. Status: {spaces_response.status_code}")
        
        self._flag_spaces = 0

        return all_spaces

    def getSpaceID(self,space_name)->int:
        """Retorna o id do espaço procurado
        """
        spaceName = space_name.upper().replace(" ","")
        space = self.getSpaces()

        for i in range(len(space)):
            space_generate = space[i]["name"]
            space_name = space_generate.upper().replace(" ","")
            if( space_name == spaceName):
                spaceID = space[i]["id"]
                break
            else:
                spaceID = 0
                
        return spaceID
    
class Folders():
    """Avaliar as pastas de um espaço
        Args:
            self.auth: autenticação
            self.space: espaço de trabalho
    """
    def __init__(self,auth:dict,space_id:int): # Removido folder_name do init
        self.auth = auth
        self.space = space_id
        self._flag_folders = True

    def getFolders(self) -> list:
        """Seleciona todas as pastas do espaço

        Returns:
            list: pastas do espaço
        """
        endpoint = f"https://api.clickup.com/api/v2/space/{self.space}/folder"
        query = {
            "archived": "false",
        }
    
        folders = requests.get(endpoint,headers=self.auth, params=query)
        folders_json = {} # Inicializa para evitar NameError
        all_folders = [] # Inicializa para evitar NameError

        if(folders.status_code == 200):
            folders_json = folders.json()
            all_folders = folders_json.get("folders", [])
            if all_folders and self._flag_folders:
                print("Pastas acessadas com sucesso:")
                for list_item in all_folders: 
                    print(f"- {list_item["name"]}")
            else:
                print("Nenhuma pasta encontrada.")
        
        else:
            print(f"Falha na conexão com a API ao acessar pastas. Status: {folders.status_code}")

        self._flag_folders = False

        return all_folders
    
    def getFolderId(self, folder_name: str) -> int: # Adicionado folder_name como parâmetro
        """Filtra apenas a pasta com o nome procurado

        Returns:
            int: id da pasta
        """
        folders = self.getFolders()
        target_folder_name_formatted = folder_name.upper().replace(" ","")
        
        for folder in folders:
            if target_folder_name_formatted == folder["name"].upper().replace(" ",""):
                return folder["id"]
        return 0 # Retorna 0 se não encontrar

        
