from flask_httpauth import HTTPBasicAuth
from src.user_info import user_info
import pandas as pd
import time

Auth = HTTPBasicAuth()

@Auth.verify_password
def verify(username,password):
    if not (username and password):
        return False
    if user_info.get(username) == password:
        return username
    return False

def registrar_uso(user,endpoint):
    record = pd.read_csv('src/record.csv')
    new_row = pd.DataFrame({'request_id':[len(record)],'user':[user],'endpoint':[endpoint],'time':[time.time()]})
    new_record = pd.concat([record,new_row])
    new_record.to_csv('src/record.csv',index = False)

def get_endpoint(obj):
    classe = str(type(obj))
    point_ = classe.find('.')
    point = classe.find('.',point_ + 1)
    aspa = classe.find("'",point)
    return classe[point + 1:aspa]