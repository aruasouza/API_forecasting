from flask_restful import Resource
from math import pi
from src.server import server
from src.parse_args import *
from src.serie_temporal import go

api = server.api

class Pi(Resource):
    def get(self):
        return {'pi':pi}

class Square(Resource):
    def get(self,number):
        return {'number':number,
        'squared':number * number}

class Math(Resource):
    def post(self):
        operacoes = ['somar','multiplicar','dividir','subtrair']
        args = calculator_args.parse_args()
        operacao = args['operacao']
        if operacao in operacoes:
            if operacao == 'somar':
                resultado = args['numero1'] + args['numero2']
            elif operacao == 'multiplicar':
                resultado = args['numero1'] * args['numero2']
            elif operacao == 'dividir':
                resultado = args['numero1'] / args['numero2']
            elif operacao == 'subtrair':
                resultado = args['numero1'] - args['numero2']
        else:
            resultado = 'Operação não permitida'
        return {'resultado':resultado}

class TimeSeries(Resource):
    def post(self):
        args = timeseries_args.parse_args()
        serie = args['timeseries']
        periodos = args['periods']
        return go(serie,periodos)


api.add_resource(Pi,'/pi')
api.add_resource(Square,'/square/<int:number>')
api.add_resource(Math,'/math')
api.add_resource(TimeSeries,'/timeseries')