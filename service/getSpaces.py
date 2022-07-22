import requests

class Spaces():
    def __init__(self,auth:dict,space_name:str,workspace_id:int) -> None:
        """Coleta os dados de todos os espaços
        Args:
            auth:{Authorization:token}
            space_name: template
            workspace_id: 0912
        """
        self.auth = auth
        self.spaceName = space_name.upper().replace(" ","")
        self.workspaceID = workspace_id
        self.endpoint = f"https://api.clickup.com/api/v2/team/{self.workspaceID}/space?archived=false"
        
    def getSpaces(self)->dict:
        """retorna todos os espaços do usuário
        """
        spaces = requests.get(self.endpoint,headers=self.auth)
        spaces_json = spaces.json()
        return(spaces_json["spaces"])

    def getSpaceID(self)->int:
        """retorna o id do espaço procurado
        """
        space = self.getSpaces()

        for i in range(len(space)):
            space_generate = space[i]["name"]
            space_name = space_generate.upper().replace(" ","")
            if( space_name == self.spaceName):
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