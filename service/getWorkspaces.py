import requests

class Workspace():
    def __init__(self,auth:dict,workspace_name:str) -> None:
        """Coletar dados de todos os workspaces do usuário
        Args:
            auth: {"Authorization": token}
            workspace_name: projete5d
        """
        self.auth = auth
        self.spaceName = workspace_name.upper().replace(" ","")
        self.endpoint="https://api.clickup.com/api/v2/team"
        
    def getWorkspaces(self)->list:
        """Coleta uma lista de workspaces existentes
        """
        workspaces = requests.get(self.endpoint,headers=self.auth)
        workspaces_json = workspaces.json()
        return(workspaces_json["teams"])

    def getWorspaceID(self)->int:
        """Retorna um inteiro do ID do workspace descrito
        """
        workspace = self.getWorkspaces()
        
        for i in range(len(workspace)):
            workspace_generate = workspace[i]["name"]
            workspace_name = workspace_generate.upper().replace(" ","")
            
            if( workspace_name == self.spaceName):
                workspaceID = workspace[i]["id"]
                break
            
            else:
                workspaceID = 0
                
        return(workspaceID)
    
    def getWorkspaceStatus(self)->int:
        """Retorna um inteiro do status da solicitação a API
        """
        endpoint = "https://api.clickup.com/api/v2/team"
        return(requests.get(endpoint,headers=self.auth).status_code)
    
    def getWorkspaceTeam(self)->list:
        """Retorna uma lista com todos os membros do workspace selecionado"""
        workspace = self.getWorkspaces()
        
        for i in range(len(workspace)):
            workspace_generate = workspace[i]["name"]
            workspace_name = workspace_generate.upper().replace(" ","")
            
            if( workspace_name == self.spaceName):
                workspaceMembers = workspace[i]["members"]
                break
            
            else:
                workspaceMembers = 0
        
        return(workspaceMembers)
    
    def getMembersID(self)->list:
        """Retorna uma lista com os ids dos membros
        """
        users = self.getWorkspaceTeam()
        idMembers = []
        
        for i in range(len(users)):
            member = users[i]["user"]
            idMembers.append(member["id"])
            
        return(idMembers)
    
    def getMembersName(self)->list:
        """Retorna uma lista com os nomes dos membros
        """
        users = self.getWorkspaceTeam()
        nameMembers = []
        
        for i in range(len(users)):
            member = users[i]["user"]
            nameMembers.append(member["username"])
            
        return(nameMembers)
    
    def getMembersEmail(self)->list:
        """Retorna uma lista com os emails dos membros
        """
        users = self.getWorkspaceTeam()
        emailMembers = []
        
        for i in range(len(users)):
            member = users[i]["user"]
            emailMembers.append(member["email"])
            
        return(emailMembers)