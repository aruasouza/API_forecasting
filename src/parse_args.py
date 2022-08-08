from flask_restful import reqparse

calculator_args = reqparse.RequestParser()

calculator_args.add_argument('operacao',type = str,help = 'Operação não especificada',required = True)
calculator_args.add_argument('numero1',type = int,help = 'Número não especificado',required = True)
calculator_args.add_argument('numero2',type = int,help = 'Número não especificado',required = True)

timeseries_args = reqparse.RequestParser()

timeseries_args.add_argument('timeseries',type = dict,required = True)
timeseries_args.add_argument('periods',type = int,required = True)
#timeseries_args.add_argument('format',type = str,required = False)