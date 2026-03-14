import requests

class List():
    def __init__(self,auth:dict,space_id:int) -> None:
        """coleta todos os dados das listas em um espaço
        Args:
            auth:{Authorization:token}
            list_name: template (se estiver em pasta usar None)
            space_id:0848
        """
        self.auth = auth
        self.spaceID = space_id
        self.endpoint = f"https://api.clickup.com/api/v2/space/{self.spaceID}/list?archived=false"
        
    def getListsFolderless(self)->list:
        """retorna todas as listas no space
        """ 
        listas = requests.get(self.endpoint,headers=self.auth)
        listas_json=listas.json()
        return(listas_json["lists"])

    def getLists(self,folderID)->list:
        """_summary_

        Args:
            folderID (_type_): _description_

        Returns:
            list: _description_
        """
        endpoint=f"https://api.clickup.com/api/v2/folder/{folderID}/list"
        query = {
            "archived": "false"
        }
        listas = requests.get(endpoint,headers=self.auth,params=query)
        
        if(listas.status_code == 200):
            listas_json = listas.json()
            print("Listas carregadas!")
        else:
            listas_json = {}
            print("Erro de conexão com a API")
        
        return(listas_json.get("lists",{}))

    def getListID(self,list_name=None,folder_id=None)->int:
        """retorna o id da lista procurada
        """
        listID = []

        if(list_name):
            listName = list_name.upper().replace(" ","")
            lists = self.getListsFolderless()
        
            for i in range(len(lists)):
                list_generate = lists[i]["name"]
                list_name = list_generate.upper().replace(" ","")
                if(list_name == listName):
                    listID.append(lists[i]["id"])
                    break
                else:
                    listID.append(0)
            
        else:

            lists = self.getLists(folder_id)

            for list in lists:
                listID.append(list["id"])

        return(listID)
    
    def getListsStatus(self)->int:
        """retorna o status da solicitação a api
        """
        endpoint = f"https://api.clickup.com/api/v2/space/{self.spaceID}/list?archived=false"
        listas = requests.get(endpoint,headers=self.auth)
        return(listas.status_code)
    
    def getCustomFields(self)->list:
        """retorna os campos personalizados da lista
        """
        list_id = self.getListID()
        endpoint = f"https://api.clickup.com/api/v2/list/{list_id}/field"
        
        custom_labels = requests.get(endpoint,headers=self.auth).json()
        
        fields = custom_labels["fields"]   

        return(fields)
    