# Definição dos endpoints

from flask_restful import Resource
from math import pi
from src.server import server
from src.parse_args import *
from src.serie_temporal import go
from src.security import registrar_uso,get_endpoint

# Criação do objeto API onde são criados os endpoints

api = server.api

# Endpoint que retorna o valor de Pi

class Pi(Resource):
    @server.auth.login_required
    def get(self):
        user = server.auth.current_user()
        endp = get_endpoint(self)
        registrar_uso(user,endp)
        return {'pi':pi}

# Endpoint que recebe um número e retorna ele ao quadrado

class Square(Resource):
    @server.auth.login_required
    def get(self,number):
        user = server.auth.current_user()
        endp = get_endpoint(self)
        registrar_uso(user,endp)
        return {'number':number,
        'squared':number * number}

# Endpoint que recebe uma série temporal e retorna a mesma série com um forecast de tempo especificado

class TimeSeries(Resource):
    @server.auth.login_required
    def post(self):
        user = server.auth.current_user()
        endp = get_endpoint(self)
        registrar_uso(user,endp)
        args = timeseries_args.parse_args()
        serie = args['timeseries']
        periodos = args['periods']
        return go(serie,periodos)


# Registro dos endpoints no objeto API

api.add_resource(Pi,'/pi')
api.add_resource(Square,'/square/<int:number>')
api.add_resource(TimeSeries,'/timeseries')