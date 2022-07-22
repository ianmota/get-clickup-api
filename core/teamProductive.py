import pandas

class ProdutividadeEquipe():
    def __init__(self,data_base:dict) -> None:
        self.database = data_base["tasks"]
        
    def getTask(self):
        return(self.database["name"])
    
    def getCreatedDate(self):
        return(self.database["date_created"])
    
    def getUpdatedDate(self):
        return(self.database["date_updated"])
    
    def getDataClosed(self):
        return(self.database["date_closed"])