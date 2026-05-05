import requests

class List():
    """Coleta todos os dados das listas em um espaço
    Args:
        auth(str):{Authorization:token}
        space_id(int):id
    """
    def __init__(self,auth:dict,space_id:int) -> None:
        self.auth = auth
        self.spaceID = space_id
        self.endpoint = f"https://api.clickup.com/api/v2/space/{self.spaceID}/list?archived=false"
        self._flag_lists = True 

    def getListsFolderless(self)->list:
        """Retorna todas as listas no space
        """       
        listas_response= requests.get(self.endpoint,headers=self.auth)

        listas_json = {} # Inicializa para evitar NameError
        allLists = [] # Inicializa para evitar NameError

        if(listas_response.status_code == 200):
            listas_json = listas_response.json()
            allLists = listas_json.get("lists", [])
            if allLists and self._flag_lists:
                self._flag_lists = False
                print("Listas acessadas com sucesso:")
                for list_item in allLists: # Renomeado para evitar conflito com a palavra-chave 'list'
                    print(f"- {list_item["name"]}")
            
        else:
            print(f"Erro de conexão com a API ao acessar listas sem pasta. Status: {listas_response.status_code}")

        return(allLists)

    def getLists(self,folderID)->list:
        """Retorna todas as listas em uma pasta

        Args:
            folderID (int): id da pasta

        Returns:
            list: _description_
        """
        endpoint=f"https://api.clickup.com/api/v2/folder/{folderID}/list"
        query = {
            "archived": "false"
        }

        listas_response = requests.get(endpoint,headers=self.auth,params=query)
        
        listas_json = {} # Inicializa para evitar NameError
        allLists = [] # Inicializa para evitar NameError
        if(listas_response.status_code == 200):
            listas_json = listas_response.json()
            allLists = listas_json.get("lists", [])
            if allLists and self._flag_lists:   
                self._flag_lists = False
                print("Listas acessadas com sucesso:")
                for list_item in allLists: # Renomeado para evitar conflito com a palavra-chave 'list'
                    print(f"- {list_item["name"]}")
            
        else:
            print(f"Erro de conexão com a API ao acessar listas em pasta. Status: {listas_response.status_code}")
        
        return(allLists)

    def getListID(self,list_name=None,folder_id=None)->int:
        """Retorna o id da lista procurada
        """
        listID = []

        if(list_name):
            target_list_name_formatted = list_name.upper().replace(" ","")
            lists = self.getListsFolderless()
        
            found_id = None
            for list_item in lists:
                current_list_name_formatted = list_item["name"].upper().replace(" ","")
                if current_list_name_formatted == target_list_name_formatted:
                    found_id = list_item["id"]
                    break
            if found_id is not None:
                listID.append(found_id)
            else:
                print(f"Aviso: Lista '{list_name}' não encontrada no espaço sem pasta.")
                listID.append(0) # Retorna 0 se não encontrar
            
        else:
            lists = self.getLists(folder_id)
            for list_item in lists:
                listID.append(list_item["id"])

        if not listID and folder_id is not None: # Se nenhuma lista foi encontrada em uma pasta específica
            print(f"Aviso: Nenhuma lista encontrada na pasta com ID '{folder_id}'.")

        return listID
    
    def getCustomFields(self)->list:
        """retorna os campos personalizados da lista
        """
        list_id = self.getListID()
        endpoint = f"https://api.clickup.com/api/v2/list/{list_id}/field"
        
        custom_labels = requests.get(endpoint,headers=self.auth).json()
        
        fields = custom_labels["fields"]   

        return(fields)
    