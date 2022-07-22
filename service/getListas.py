import requests

class List():
    def __init__(self,auth:dict,list_name:str,space_id:int) -> None:
        """coleta todos os dados das listas em um espaço
        Args:
            auth:{Authorization:token}
            list_name: template
            space_id:0848
        """
        self.auth = auth
        self.listName = list_name.upper().replace(" ","")
        self.spaceID = space_id
        self.endpoint = endpoint = f"https://api.clickup.com/api/v2/space/{self.spaceID}/list?archived=false"
        
    def getListsFolderless(self)->list:
        """retorna todas as listas no space
        """ 
        listas = requests.get(self.endpoint,headers=self.auth)
        listas_json=listas.json()
        return(listas_json["lists"])

    def getListID(self)->int:
        """retorna o id da lista procurada
        """
        list = self.getListsFolderless()
        
        for i in range(len(list)):
            list_generate = list[i]["name"]
            list_name = list_generate.upper().replace(" ","")
            if(list_name == self.listName):
                listID = list[i]["id"]
                break
            else:
                listID = 0
            
        return(listID)
    
    def getListsStatus(self)->int:
        """retorna o status da solicitação a api
        """
        endpoint = f"https://api.clickup.com/api/v2/space/{self.spaceID}/list?archived=false"
        listas = requests.get(endpoint,headers=self.auth)
        return(listas.status_code)
    
    def getEmpreendimentos(self):
        list_id = self.getListID()
        endpoint = f"https://api.clickup.com/api/v2/list/{list_id}/field"
        
        custom_labels = requests.get(endpoint,headers=self.auth).json()
        
        fields = custom_labels["fields"]   
        
        for i in range(len(fields)):
            if(fields[i]["name"] == "Empreendimento"):
                customFields = fields[i]["type_config"]["options"]
                break
            else:
                customFields = 0
        print(customFields)
        