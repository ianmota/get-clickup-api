import requests
from datetime import datetime

class Workspace():
    def __init__(self,auth:dict,workspace_name:str) -> None:
        """Coletar dados de todos os workspaces do usuário
        Args:
            auth: dados de autorização
            workspace_name: nome do espaço
        """
        self.auth = auth
        self.spaceName = workspace_name.upper().replace(" ","")
        self.endpoint="https://api.clickup.com/api/v2/team"
        
    def getWorkspaces(self)->list:
        """Coleta uma lista de workspaces existentes
        """
        workspaces = requests.get(self.endpoint,headers=self.auth)
        if(workspaces.status_code == 200):
            workspaces_json = workspaces.json()
            print(f"Workspace {self.spaceName} acessado!")
            
        else:
            print(f"Erro na comunicação com o workspace {self.spaceName}!")

        return(workspaces_json.get("teams",{}))

    def getWorkspaceID(self)->int:
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
    
    def getTimeEntries(self,list_ids:list,s_date:str=None, e_date:str=None)->list:
        """Retorna uma lista com todas as entradas de dados dos membros do workspace em uma determinada lista

        Args:
            list_id (int): ID da lista
            s_date (str): Range inicial para coleta no formato 01/02/1900 
            e_date (str): Range final para coleta no formato 01/02/1900

        Returns:
            list: Dados de entrada de dados
        """
        workspace_id = self.getWorkspaceID()
        if not workspace_id:
            print("Não foi possível obter o ID do Workspace. Abortando a coleta de tempo.")
            return []
            
        url = f"{self.endpoint}/{workspace_id}/time_entries"
        all_time = []
        
        if s_date:
            s_ms = int(datetime.strptime(s_date, "%d/%m/%Y").timestamp()*1000)
        else:
            s_ms = int(datetime.strptime("10/02/2024","%d/%m/%Y").timestamp()*1000)
            
        if e_date:
            end_ms = int(datetime.strptime(e_date, "%d/%m/%Y").timestamp()*1000)
        else:
            end_ms = int(datetime.now().timestamp()*1000)

        assignees_str = ",".join(map(str,self.getMembersID()))


        for list_id in list_ids:
            query = {
                "list_id": list_id,
                "start_date": s_ms,
                "end_date": end_ms,
                "assignee": assignees_str
            }

            time_request = requests.get(url=url, headers=self.auth, params=query)
            
            if time_request.status_code == 200:
                data = time_request.json().get("data", [])
                all_time.extend(data)
                print(f"Coleta de entrada de dados ({list_id}): Realizado com sucesso! {len(data)} entradas encontradas.")
            else:
                print(f"Coleta de entrada de dados ({list_id}): Não realizado. Erro {time_request.status_code} na API. Resposta: {time_request.text}")

        return all_time