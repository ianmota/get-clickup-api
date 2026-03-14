import json

class serviceEasiest():
    """Esta classe é utilizada para ler arquivos importantes e salvar logs do processo

    Args:
        path (path): caminho do arquivo a ser lido/salvo
    """
    
    def __init__(self, path):
        self.path = path

    def jsonRead(self, name):
        """ Leitura de qualquer json

        Args: 
            name (str): nome do arquivo
        """
        # try:
        with open(f"{self.path}/{name}.json",'r',encoding="utf-8") as credenciais:
            dic = json.load(credenciais)

        print(f"{name} lido com sucesso!")

        # except:
        #     dic = []
        #     print(f"Problema com a leitura de {name}!")

        return dic
    
    def logSave(self,name, data):
        """Salvamento de dados importantes
        
        Args:
            data: parâmetro de dados
            name: nome do arquivo
        """
        try:
            with open(f"{self.path}/{name}.json","w",encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            
            print(f"{name} salvo com sucesso!")
        
        except:
            print(f"{name} não salvo! Verifique")