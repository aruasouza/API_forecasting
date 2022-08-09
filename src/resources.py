from flask_restful import Resource
from math import pi
from src.server import server
from src.parse_args import *
from src.serie_temporal import go
from src.security import registrar_uso,get_endpoint

api = server.api

class Pi(Resource):
    def get(self):
        user = server.auth.current_user()
        endp = get_endpoint(self)
        registrar_uso(user,endp)
        return {'pi':pi}

class Square(Resource):
    @server.auth.login_required
    def get(self,number):
        user = server.auth.current_user()
        endp = get_endpoint(self)
        registrar_uso(user,endp)
        return {'number':number,
        'squared':number * number}

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


api.add_resource(Pi,'/pi')
api.add_resource(Square,'/square/<int:number>')
api.add_resource(TimeSeries,'/timeseries')