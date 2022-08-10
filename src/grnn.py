# Funções de treinamento e predição utilizando GRNN

from src.scripts import serie_estocastica,convert_prediction_estocastica,convert_prediction_log
import numpy as np
from pyGRNN import GRNN

# Função utilizada quando há tendencia E sazonalidade

def trend_and_sazon(x_train,x_fut,y):
    y_ = serie_estocastica(y)
    minimo = abs(min(y_))
    y_train = np.array([valor + minimo for valor in y_])
    AGRNN = GRNN()
    AGRNN.fit(x_train, y_train)
    y_pred = AGRNN.predict(x_fut)
    return convert_prediction_estocastica(y[-1],[valor - minimo for valor in y_pred])

# Função utilizada quando há tendencia mas não sazonalidade

def trend_and_not_sazon(x_train,x_fut,y,sem_trend,popt):
    minimo = abs(min(sem_trend))
    y_train = np.array([valor + minimo for valor in sem_trend])
    AGRNN = GRNN()
    AGRNN.fit(x_train, y_train)
    y_pred = AGRNN.predict(x_fut)
    return convert_prediction_log(y,[valor - minimo for valor in y_pred],popt)

# Função utilizada quando não há tendencia

def not_trend(x_train,x_fut,y):
    y_train = np.array(y)
    AGRNN = GRNN()
    AGRNN.fit(x_train, y_train)
    return AGRNN.predict(x_fut)