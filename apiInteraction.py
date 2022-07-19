from service.getWorkspaces import Workspace
from service.credentialRead import credentialRead
from service.getSpaces import Spaces
from service.getListas import List
from service.getTasks import Tasks

credenciais = credentialRead("credenciais.json")
token = credenciais["token"]
header = {"Authorization": token["lucas-ffaf"]}

workspaces_get = Workspace(header,"projete 5d")
status_workspace = workspaces_get.getWorkspaceStatus()
workspace_id = workspaces_get.getWorspaceID()

spaces_get = Spaces(header,"templates projete 5d",workspace_id)
status_space = spaces_get.getSpacesStatus()
space_id = spaces_get.getSpaceID()

lista_get = List(header,"005 - PROJETE 5D GESTÃO À VISTA ",space_id)
status_list = lista_get.getListsStatus()
list_id = lista_get.getListID()

tasks_get = Tasks(header,list_id)
status_task = tasks_get.getTasksStatus()
task_json = tasks_get.getTasks()

print(task_json)
