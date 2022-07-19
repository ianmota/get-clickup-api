import requests

class Tasks():
    def __init__(self,auth:dict,list_id:int) -> None:
        self.auth = auth
        self.listID = list_id
        
    def getTasks(self):
        endpoint = f"https://api.clickup.com/api/v2/list/{self.listID}/task?archived=false"
        tasks = requests.get(endpoint,headers=self.auth)
        tasks_json = tasks.json()
        return(tasks_json["tasks"])
    
    def getTasksStatus(self):
        endpoint = f"https://api.clickup.com/api/v2/list/{self.listID}/task?archived=false"
        tasks = requests.get(endpoint,headers=self.auth)
        return(tasks.status_code)
    