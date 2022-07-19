import json

def credentialRead(path):
    with open(path,'r') as credenciais:
        dic = json.load(credenciais)
    
    return dic