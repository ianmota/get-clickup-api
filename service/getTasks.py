import requests
import time
from datetime import datetime

class Tasks():
    def __init__(self,auth:dict,list_id:int,) -> None:
        self.auth = auth
        self.listID = list_id # Este é esperado ser uma lista de IDs de listas

    def getTasks(self, start_date:str=None):

        tasks_json = []
        

        if start_date:
            start_ms = int(datetime.strptime(start_date, "%d/%m/%Y").timestamp()*1000)

        else:
            start_ms = int(datetime.strptime("10/02/2024","%d/%m/%Y").timestamp()*1000)
        
        for listID in self.listID:
            endpoint = f"https://api.clickup.com/api/v2/list/{listID}/task"
            
            page = 0
            flag_search = True
            limit_exceed = True

            while True:
                query = {
                "include_closed": "true",
                "include_subtasks": "true",
                "subtasks":"true",
                "page": page,
                "date_updated_gt": start_ms
                    }
                tasks = requests.get(endpoint,headers=self.auth, params=query)
                
                if tasks.status_code == 200:
                    tasks_data = tasks.json()
                    page_tasks = tasks_data.get("tasks", [])

                    if not page_tasks: # Nenhuma tarefa restante para esta lista ou nenhuma tarefa encontrada
                        flag_search = False
                        print(f"Coleta de tarefas para a lista {listID}: Concluída ou nenhuma tarefa encontrada.")

                    elif page >= 20:
                        limit_exceed = False
                        print("ATENÇÃO! O processo foi interrompido pelo limite de iterações.")

                    else:
                        tasks_json.extend(page_tasks)
                        page+=1
                        time.sleep(0.1)

                else:
                    print(f"Erro na API ao coletar tarefas para a lista {listID}: {tasks.status_code}. Resposta: {tasks.text}")
                    break

                if not (flag_search and limit_exceed):
                    break
        
        return tasks_json
    
    def getTasksID(self):
        tasks = self.getTasks()
        id_tasks = []
        
        for i in range(len(tasks)):
            id_tasks.append(tasks[i]["id"])
            
        return(id_tasks)
    
    def lastSave(self):
        return(datetime.now().strftime("%d/%m/%Y"))
    