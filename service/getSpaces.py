import requests

class Spaces():
    def __init__(self,auth:dict,workspace_id:int) -> None:
        """Coleta os dados de todos os espaços
        Args:
            auth:{Authorization:token}
            space_name: template
            workspace_id: 0912
        """
        self.auth = auth
        self.workspaceID = workspace_id
        self.endpoint = f"https://api.clickup.com/api/v2/team/{self.workspaceID}/space?archived=false"
        
    def getSpaces(self)->list:
        """retorna uma lista com todos os espaços do usuário
        """
        spaces = requests.get(self.endpoint,headers=self.auth)
        if(spaces.status_code == 200):
            spaces_json = spaces.json()
            print("Espaço acessado com sucesso!")
        else:
            print("Erro na conexão com a API ao acessar os espaços")
        return(spaces_json.get("spaces",{}))

    def getSpaceID(self,space_name)->int:
        """retorna o id do espaço procurado
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
                
        return(spaceID)
    
    def getSpacesStatus(self)->int:
        """retorna o status da solicitação a api
        """
        endpoint = f"https://api.clickup.com/api/v2/team/{self.workspaceID}/space?archived=false"
        spaces = requests.get(endpoint,headers=self.auth)
        return(spaces.status_code)
    
class Folders():
    """Avaliar as pastas de um espaço
        Args:
            self.auth: autenticação
            self.folderName: pasta procurada
            self.space: espaço de trabalho
    """
    def __init__(self,auth:dict,folder_name:str,workspace_id:int):
        self.auth = auth
        self.folderName = folder_name.upper().replace(" ","")
        self.space = workspace_id

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

        if(folders.status_code == 200):
            folders_json = folders.json()
            print("Pastas acessadas!")
        
        else:
            print("Falha na conexão com a API")
        
        return(folders_json.get("folders",{}))
    
    def getFolderId(self) -> int:
        """Filtra apenas a pasta com o nome procurado

        Returns:
            int: id da pasta
        """
        folders = self.getFolders()
        folder_ID = 0
        
        for folder in folders:
            
            if(self.folderName == folder["name"].upper().replace(" ","")):
                folder_ID = folder["id"]

        
        return(folder_ID)

        

