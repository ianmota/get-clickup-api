import requests

class Spaces():
    def __init__(self,auth:dict,space_name:str,workspace_id:int) -> None:
        self.auth = auth
        self.spaceName = space_name.upper()
        self.workspaceID = workspace_id
        
    def getSpaces(self):
        endpoint = f"https://api.clickup.com/api/v2/team/{self.workspaceID}/space?archived=false"
        spaces = requests.get(endpoint,headers=self.auth)
        spaces_json = spaces.json()
        return(spaces_json["spaces"])

    def getSpaceID(self):
        space = self.getSpaces()
        
        for i in range(len(space)):
            if(space[i]["name"] == self.spaceName):
                spaceID = space[i]["id"]
                break
            else:
                spaceID = 0
                
        return(spaceID)
    
    def getSpacesStatus(self):
        endpoint = f"https://api.clickup.com/api/v2/team/{self.workspaceID}/space?archived=false"
        spaces = requests.get(endpoint,headers=self.auth)
        return(spaces.status_code)