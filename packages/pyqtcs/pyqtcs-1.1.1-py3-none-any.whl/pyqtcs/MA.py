# -*- coding:utf-8 -*-

import numpy as np
import numba as nb
from numba import jit


@jit(nopython=True)
def MA(Series, M, padding=None):
    """
    简单移动平均
    用法:MA(Series,M),Series的M日简单移动平均
    :param Series:
    :param M:
    :param padding:填充类型
    :return:ma
    """
    len_series = len(Series)
    ma = []
    for i in range(len_series - M + 1):
        ma.append(Series[i:i + M].mean())

    if padding is None:
        return np.array(ma)

    pad_num = len_series - len(ma)
    if padding == 'pre':
        return np.array(np.pad(ma, (pad_num, 0), 'constant', constant_values=(ma[0], 0)))
    elif padding == 'zero':
        return np.array(np.pad(ma, (pad_num, 0), 'constant', constant_values=(0, 0)))
    elif padding == 'nan':
        return np.array(np.pad(ma, (pad_num, 0), 'constant', constant_values=(np.NAN, 0)))
    return np.array(ma)

