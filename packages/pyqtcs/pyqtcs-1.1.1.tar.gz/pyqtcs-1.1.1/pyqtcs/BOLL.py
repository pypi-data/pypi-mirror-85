import numpy as np
import talib as ta
import pandas as pd
import numba as nb
from numba import jit
from MA import *


# @jit(nopython=True)
def BOLL(Series, M, N, padding=None):
    mid = MA(Series, M, padding)
    len_series = len(Series)
    close_series = []
    for i in range(len_series - M + 1):
        close_series.append(Series[i:i + M])

    upper = mid + N * np.std(close_series)
    lower = mid - N * np.std(close_series)
    return upper, mid, lower


def talib_boll(close, m, n):
    return ta.BBANDS(close, timeperiod=m, nbdevup=n, nbdevdn=n, matype=0)


def getBBands(df, period=10, stdNbr=2):
    try:
        close = df['close']
    except Exception as ex:
        return None

    try:
        upper, middle, lower = ta.BBANDS(
            close.values,
            timeperiod=period,
            # number of non-biased standard deviations from the mean
            nbdevup=stdNbr,
            nbdevdn=stdNbr,
            # Moving average type: simple moving average here
            matype=0)
    except Exception as ex:
        return None

    data = dict(upper=upper, middle=middle, lower=lower)
    df = pd.DataFrame(data, index=df.index, columns=['upper', 'middle', 'lower']).dropna()

    return df
