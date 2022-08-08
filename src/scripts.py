import statsmodels.api as sm
import math
from scipy.optimize import curve_fit
from dateutil.relativedelta import relativedelta
from datetime import timedelta
from sklearn import preprocessing
import numpy as np


def verify_vibration(serie):
    est = np.array(serie_estocastica(preprocessing.minmax_scale(serie)))
    vib = est.std()
    return vib > 0.05

def autocorrelation(values,intervalo):
    if 28 < intervalo < 32:
        acorr = sm.tsa.acf(values, nlags = 12)
        auto = [acorr[12]]
    elif 6 < intervalo < 8:
        acorr = sm.tsa.acf(values, nlags = 52)
        auto = [acorr[4],acorr[52]]
    elif intervalo > 32:
        auto = [0]
    else:
        ano = round(365/intervalo)
        mes = round(31/intervalo)
        acorr = sm.tsa.acf(values, nlags = ano)
        auto = [acorr[mes],acorr[ano]]
    auto = [abs(valor) for valor in auto]
    print('Seasonality test result:',max(auto))
    return max(auto)

def serie_estocastica(values):
    values = list(values)
    new_values = [0]
    for i in range(1,len(values)):
        new_values.append(values[i] - values[i - 1])
    return new_values

def convert_prediction_estocastica(last_value,predictions):
    predictions = list(predictions)
    new_pred = [last_value]
    for i in range(len(predictions)):
        new_pred.append(new_pred[-1] + predictions[i])
    return new_pred[1:]

def convert_prediction_log(y,predictions,popt):
    len_y = len(y)
    len_p = len(predictions)
    new_pred = [predictions[i - len_y] + square(i,popt[0],popt[1],popt[2]) for i in range(len_y,len_y + len_p)]
    exp = [math.exp(valor) for valor in new_pred]
    estocastica = serie_estocastica(exp)
    return convert_prediction_estocastica(y[-1],estocastica)

def monday(x):
    if x == 6:
        return 1
    return 0

def linear(x,a,b):
    return (a * x) + b

def square(x,a,b,c):
    return (a * (x ** 2)) + (b * x) + c

def fit(xdata,ydata,func):
    x = list(xdata)
    y = list(ydata)
    popt,pcov = curve_fit(func,x,y)
    return popt

def intervalo_medio(datas):
    datas.sort_values()
    intervalos = []
    for i in range(1,len(datas)):
        delta = datas[i] - datas[i - 1]
        intervalos.append(delta.days)
    return sum(intervalos) / len(intervalos)

def criar_tempo(periodos,intervalo,start):
    datas = [start]
    for i in range(periodos):
        if 28 < intervalo < 32:
            new_data = datas[-1] + relativedelta(months = 1)
        elif 6 < intervalo < 8:
            new_data = datas[-1] + timedelta(weeks = 1)
        elif 360 < intervalo < 370:
            new_data = datas[-1] + relativedelta(years = 1)
        else:
            new_data = datas[-1] + timedelta(days = intervalo)
        datas.append(new_data)
    return datas[1:]