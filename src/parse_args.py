# Criação dos argumentos exigidos no uso da API

from flask_restful import reqparse

timeseries_args = reqparse.RequestParser()

timeseries_args.add_argument('timeseries',type = dict,required = True)
timeseries_args.add_argument('periods',type = int,required = True)