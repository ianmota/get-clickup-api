from openpyxl import load_workbook
from openpyxl.utils.dataframe import dataframe_to_rows
import pandas as pd
import os
from datetime import datetime

class dataConstructor():
    """Responsável pela extração dos dados importantes dos arquivos de logs obtidos ao longo do processo e salvar no excel

    Args:
        data(json): dados extraídos com todas as tasks
    """
    
    def __init__(self, data):
       self.data = data

    def data_taskExtract(self):
        """Seleciona apenas os parâmetros importantes de todas as tasks coletadas. A entrada de horas é captada de maneira total (não da para 
        filtrar por semana, por exemplo)

        Returns:
            dictionary: dicionário com informações reduzidas
        """
        extracted_data = []
        
        for task in self.data:
            row = {
                "Atividade": task.get("name"),
                "Responsável": ", ".join([a['username'] for a in task.get('assignees', [])]),
                "Status": task.get("status",{}).get("status"),
                "Tempo gasto (ms)": task.get("time_spent") or 0
            }

            for field in task.get("custom_fields",[]):
                field_name = field.get("name")

                if field.get("type") == "drop_down":
                    value_index = field.get("value")

                    if value_index is not None:
                        options = field.get("type_config",{}).get("options",[])

                        try:
                            selected_option = options[int(value_index)]
                            row[field_name] = selected_option.get("name")
                        
                        except (IndexError, ValueError):
                            row[field_name] = None
                    
                    else:
                        row[field_name] = None
                
                else:
                    row[field_name] = field.get("value", None)
            
            extracted_data.append(row)
        
        return extracted_data
    
    def timeEntrieExtract(self,entry_data):
        """Seleciona apenas os parâmetros importantes de todas as tasks coletadas. A entrada de horas é captada de parcialmente (conseguimos
        usar um filtro temporal)

        Returns:
            dictionary: dicionário com informações reduzidas
        """
        extracted_data = []
        tasks_lookup = {}

        for task in self.data:
            tasks_lookup[task["id"]] = {
                "Atividade": task.get("name"),
                "Responsável_tarefa": ", ".join([a['username'] for a in task.get('assignees', [])]),
                "Status": task.get("status",{}).get("status"),
            }

            for field in task.get("custom_fields",[]):
                field_name = field.get("name")

                if field.get("type") == "drop_down":
                    value_index = field.get("value")

                    if value_index is not None:
                        options = field.get("type_config",{}).get("options",[])

                        try:
                            selected_option = options[int(value_index)]
                            tasks_lookup[task["id"]][field_name] = selected_option.get("name")
                        
                        except (IndexError, ValueError):
                            tasks_lookup[task["id"]][field_name] = None
                    
                    else:
                        tasks_lookup[task["id"]][field_name] = None
                
                else:
                    tasks_lookup[task["id"]][field_name] = field.get("value", None)

        extraction_date = datetime.now().strftime("%d/%m/%Y")
        tasks_with_entries = set()
        
        for entry in entry_data: 
            t_id = entry.get("task",{}).get("id")
            detalhes = tasks_lookup.get(t_id) 
            
            if detalhes:
                tasks_with_entries.add(t_id)
                extracted_data.append({
                    "Atividade": detalhes.get("Atividade"),
                    "Responsável_tarefa": detalhes.get("Responsável_tarefa"),
                    "Responsável_tempo": entry.get("user",{}).get("username"),
                    "Status": detalhes.get("Status"),
                    "Tempo (ms)": int(entry.get("duration", 0)),
                    "Fase": detalhes.get("Fase"),
                    "Projetos": detalhes.get("Projetos - Norcore"),
                    "data_extraido": extraction_date,
                    "data_alterado": datetime.fromtimestamp(int(entry["at"]) / 1000).strftime("%d/%m/%Y") if entry.get("at") else None,
                    "serviço": detalhes.get("Serviços")
                })

        # Adiciona as tarefas que não tiveram contagem de horas registrada
        for t_id, detalhes in tasks_lookup.items():
            if t_id not in tasks_with_entries:
                extracted_data.append({
                    "Atividade": detalhes.get("Atividade"),
                    "Responsável_tarefa": detalhes.get("Responsável_tarefa"),
                    "Responsável_tempo": None,
                    "Status": detalhes.get("Status"),
                    "Tempo (ms)": 0,
                    "Fase": detalhes.get("Fase"),
                    "Projetos": detalhes.get("Projetos - Norcore"),
                    "data_extraido": extraction_date,
                    "data_alterado": None,
                    "serviço": detalhes.get("Serviços")
                })

        return extracted_data

    def excelSave(self,json_file, path):
        df = pd.DataFrame(json_file)

        nome_planilha = "Dados"
        nome_tabela = "data"
        wb = load_workbook(path)
        ws = wb[nome_planilha]
        tabela = ws.tables[nome_tabela]

        try: 
            if not os.path.exists(path):
                print("Arquivo não criado. Não existe um excel neste caminho!")
                return
            
            for row in ws.iter_rows(min_row=2, max_row=ws.max_row):
                for cell in row:
                    cell.value = None
            
            for r_idx, row in enumerate(dataframe_to_rows(df, index=False, header=False),start=2):
                for c_idx, value in enumerate(row,start=1):
                    ws.cell(row=r_idx,column=c_idx, value=value)

            last_column = chr(64+len(df.columns))
            last_line = len(df) + 1
            new_range = f"A1:{last_column}{last_line}"
            tabela.ref = new_range

            if tabela.autoFilter:
                tabela.autoFilter.ref = new_range
                
            wb.save(path)
            print("Arquivo salvo com sucesso!")

        except (PermissionError):
            print("Feche o arquivo e tente novamente!")