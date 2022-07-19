import requests

class List():
    def __init__(self,auth:dict,list_name:str,space_id:int) -> None:
        self.auth = auth
        self.listName = list_name.upper()
        self.spaceID = space_id
        
    def getListsFolderless(self):
        endpoint = f"https://api.clickup.com/api/v2/space/{self.spaceID}/list?archived=false"
        listas = requests.get(endpoint,headers=self.auth)
        listas_json=listas.json()
        return(listas_json["lists"])

    def getListID(self):
        list = self.getListsFolderless()
        
        for i in range(len(list)):
            if(list[i]["name"] == self.listName):
                listID = list[i]["id"]
                break
            else:
                listID = 0
            
        return(listID)
    
    def getListsStatus(self):
        endpoint = f"https://api.clickup.com/api/v2/space/{self.spaceID}/list?archived=false"
        listas = requests.get(endpoint,headers=self.auth)
        return(listas.status_code)