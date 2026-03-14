from service.getWorkspaces import Workspace
from service.credentialRead import serviceEasiest
from service.getSpaces import Spaces, Folders
from service.getListas import List
from service.getTasks import Tasks
from database.excelConstructor import dataConstructor

srvc_log = serviceEasiest("logs") #open the log path

credenciais = srvc_log.jsonRead("credenciais") #security information
header = {
    "Authorization": credenciais["token"]
    }

caminho_excel = credenciais["path"]

workspaces_get = Workspace(header,"norcore") #open workspace indicated
workspace_id = workspaces_get.getWorkspaceID()

spaces_get = Spaces(header,workspace_id) #open all spaces from workspace indicated
all_spaces = spaces_get.getSpaces()

space_id_andamento = spaces_get.getSpaceID("andamento") 

space_id_planejamento = spaces_get.getSpaceID("planejamento")

folders_get_b55 = Folders(header,"Planejamento projetos - B55",space_id_planejamento) #open lists of b55
folder_id_b55 = folders_get_b55.getFolderId()

folders_get_norcore = Folders(header, "Planejamento projetos - Interno", space_id_planejamento) #open norcore lists
folder_id_norcore = folders_get_norcore.getFolderId()

folders_get_estudos = Folders(header, "Estudos", space_id_planejamento) #open study lists
folder_id_estudos = folders_get_norcore.getFolderId()

lista_get_andamento = List(header,space_id_andamento) #get olds list ids 
list_id_semanal = lista_get_andamento.getListID(list_name="semanal")

list_get_planejamento = List(header,space_id_planejamento) #get list ids of b55
list_id_planejamento = list_get_planejamento.getListID(folder_id=folder_id_b55)
list_id_norcore = list_get_planejamento.getListID(folder_id=folder_id_norcore)
list_id_estudos = list_get_planejamento.getListID(folder_id=folder_id_estudos)

list_id = []
list_id.extend(list_id_semanal)
list_id.extend(list_id_planejamento)
list_id.extend(list_id_norcore)
list_id.extend(list_id_estudos)

tasks_get = Tasks(header,list_id)
all_tasks = tasks_get.getTasks()
tasksID = tasks_get.getTasksID()

data_time = workspaces_get.getTimeEntries(list_id)

log_geral = {
    "last_date": tasks_get.lastSave()
}


srvc_log.logSave("tasks",all_tasks) #save all tasks
srvc_log.logSave("time_entries",data_time) #save all times entries
srvc_log.logSave("use_log",log_geral) #save informations for extraction

dataExtract = dataConstructor(all_tasks)
importantData = dataExtract.timeEntrieExtract(data_time)
srvc_log.logSave("extracted_data",importantData)

dataExtract.excelSave(importantData, caminho_excel)



