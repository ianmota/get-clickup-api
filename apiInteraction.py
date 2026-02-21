from ast import Sub
from service.getWorkspaces import Workspace
from service.credentialRead import credentialRead
from service.getSpaces import Spaces
from service.getListas import List
from service.getTasks import Tasks
from service.getSubtasks import Subtasks
import json

credenciais = credentialRead("credenciais.json")
#token = credenciais["token"]
header = {
    "Authorization": credenciais["token"]
    }

workspaces_get = Workspace(header,"norcore")
status_workspace = workspaces_get.getWorkspaceStatus()
workspace_id = workspaces_get.getWorspaceID()

spaces_get = Spaces(header,"andamento",workspace_id)
all_spaces = spaces_get.getSpaces()
status_space = spaces_get.getSpacesStatus()
space_id = spaces_get.getSpaceID()

lista_get = List(header,"semanal",space_id)
status_list = lista_get.getListsStatus()
list_id = lista_get.getListID()

tasks_get = Tasks(header,list_id)
all_tasks = tasks_get.getTasks()
status_task = tasks_get.getTasksStatus()
tasksID = tasks_get.getTasksID()

with open("logs/workspaces.json","w",encoding="utf-8") as f:
    json.dump(all_tasks, f, indent=4, ensure_ascii=False)

subtasks = []
for taskid in tasksID:
    subtask_get = Subtasks(header,taskid)
    status_subtask = subtask_get.getSubtasksStatus()
    subtasks.append(subtask_get.getSubtasks()) 

print(subtasks)
