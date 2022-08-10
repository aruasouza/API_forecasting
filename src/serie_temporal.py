# Função que recebe a série temporal e retorna a predição

import numpy as np
import pandas as pd
from sklearn import preprocessing
import numpy as np
from sklearn.model_selection import GridSearchCV
from src.scripts import *
import src.grnn as gr


def go(series,periodos):

    # Separação dos valores em arrays

    datas = []
    y = []
    for data in series:
        datas.append(data)
        y.append(series[data])
    datas = pd.to_datetime(datas)
    del(series)

    # Verificar vibração

    if verify_vibration(y):
        dataset = pd.DataFrame({'y':y},index = datas).resample('w').sum()
        y = list(dataset['y'])
        datas = dataset.index
        del(dataset)
        periodos = int(periodos / 7)

    # Criação do dataframe de treinamento

    df = pd.DataFrame({})
    df['1'] = [data.day for data in datas]
    df['2'] = [data.dayofweek for data in datas]
    df['3'] = [data.month for data in datas]
    df['4'] = [data.year for data in datas]
    df['5'] = [data.quarter for data in datas]
    df['6'] = [data.day_of_year for data in datas]
    df['7'] = [data.week for data in datas]
    df['8'] = [monday(data) for data in df['2']]
    df = df.reset_index()

    # Criação do dataframe futuro

    intervalo = round(intervalo_medio(datas))
    new_datas = criar_tempo(periodos,intervalo,datas[-1])
    predict_df = pd.DataFrame({})
    predict_df['index'] = list(range(len(df),len(df) + len(new_datas)))
    predict_df['1'] = [data.day for data in new_datas]
    predict_df['2'] = [data.dayofweek for data in new_datas]
    predict_df['3'] = [data.month for data in new_datas]
    predict_df['4'] = [data.year for data in new_datas]
    predict_df['5'] = [data.quarter for data in new_datas]
    predict_df['6'] = [data.day_of_year for data in new_datas]
    predict_df['7'] = [data.week for data in new_datas]
    predict_df['8'] = [monday(data) for data in predict_df['2']]

    # Detecção de trend

    corr = np.corrcoef(np.array(y),np.arange(0,len(y)))[0,1]
    print('Trend test result:',corr)
    trend = corr < -0.6 or corr > 0.6

    # Detecção de sazonalidade

    sazon = False
    if trend:
        log = [math.log(valor) for valor in y]
        popt = fit(list(range(len(log))),log,square)
        sem_trend = [log[i] - square(i,popt[0],popt[1],popt[2]) for i in range(len(log))]
        sazon = autocorrelation(sem_trend,intervalo) > 0.5

    # Preparação das variáveis para processamento

    last_index = len(df)
    final_df = pd.concat([df,predict_df]).reset_index(drop = True)
    print(final_df.iloc[last_index - 5:last_index + 5])
    x = final_df.values
    x_processado = preprocessing.minmax_scale(final_df.values)
    x_fut = x_processado[last_index:]
    x_train = x_processado[:last_index]

    # Treinamento e predição

    if trend and sazon:
        print('Trend and seasonality detected')
        pred_trend = gr.trend_and_sazon(x_train,x_fut,y)
    elif trend and not sazon:
        print('Trend detected and seasonality not detected')
        pred_trend = gr.trend_and_not_sazon(x_train,x_fut,y,sem_trend,popt)
    else:
        print('Trend not detected')
        pred_trend = gr.not_trend(x_train,x_fut,y)

    # Preparação dos dados para retorno

    serie = pd.concat([pd.DataFrame({'data':datas,'y':y}),pd.DataFrame({'data':new_datas,'y':pred_trend})])
    serie['data'] = [str(data) for data in serie['data']]
    resposta = {}
    for i in range(len(serie)):
        resposta[serie['data'].iloc[i]] = float(serie['y'].iloc[i])
    return resposta