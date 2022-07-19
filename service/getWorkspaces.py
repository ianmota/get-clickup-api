import requests

class Workspace():
    def __init__(self,auth:dict,space_name:str) -> None:
        self.auth = auth
        self.spaceName = space_name.upper()
        
    def getWorkspaces(self):
        endpoint = "https://api.clickup.com/api/v2/team"
        workspaces = requests.get(endpoint,headers=self.auth)
        workspaces_json = workspaces.json()
        return(workspaces_json["teams"])

    def getWorspaceID(self):
        workspace = self.getWorkspaces()
        
        for i in range(len(workspace)):
            if(workspace[i]["name"] == self.spaceName):
                workspaceID = workspace[i]["id"]
                break
            
            else:
                workspaceID = 0
                
        return(workspaceID)
    
    def getWorkspaceStatus(self):
        endpoint = "https://api.clickup.com/api/v2/team"
        return(requests.get(endpoint,headers=self.auth).status_code)