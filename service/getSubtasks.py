import requests

class Subtasks():
    def __init__(self,auth,tasks_id:str) -> None:
        self.taksId = tasks_id
        self.auth = auth
        self.endpoint = f"https://api.clickup.com/api/v2/task/{self.taksId}/?include_subtasks=true"
        
    def getSubtasks(self):
        subtasks = requests.get(self.endpoint,headers=self.auth)
        subtasks_json = subtasks.json()
        return(subtasks_json)
    
    def getSubtasksStatus(self):
        subtasks = requests.get(self.endpoint,headers=self.auth)
        return(subtasks.status_code)
    
    def getSubtaskName(self):
        subtasks_json = self.getSubtasks()
        return(subtasks_json["subtasks"])
        