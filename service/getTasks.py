import requests

class Tasks():
    def __init__(self,auth:dict,list_id:int) -> None:
        self.auth = auth
        self.listID = list_id
        self.endpoint = f"https://api.clickup.com/api/v2/list/{self.listID}/task?archived=false"
        
    def getTasks(self):
        tasks = requests.get(self.endpoint,headers=self.auth)
        tasks_json = tasks.json()
        return(tasks_json["tasks"])
    
    def getTasksStatus(self):
        tasks = requests.get(self.endpoint,headers=self.auth)
        return(tasks.status_code)
    
    def getTasksID(self):
        tasks = self.getTasks()
        id_tasks = []
        
        for i in range(len(tasks)):
            id_tasks.append(tasks[i]["id"])
            
        return(id_tasks)
    
    def getTaskswithsubtasks(self):
        f"https://api.clickup.com/api/v2/list/{self.listID}/task?archived=false&subtasks=true"
        tasks = requests.get(self.endpoint,headers=self.auth)
        return(tasks.json())
        
    