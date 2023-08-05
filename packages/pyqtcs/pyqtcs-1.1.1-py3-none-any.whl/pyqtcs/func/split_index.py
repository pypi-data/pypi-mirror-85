# -*- coding:utf-8 -*-
import re

from pyqtcs.func.func import is_number

__mathstr = ['np.sin', 'np.cos', 'np.tan', 'sin', 'cos', 'tan']
__equalstr = ['>', '>=', '==', '<=', '<']


def get_split_index(formual):
    """
    将公式拆分成只包含技术指标的list
    @param formual: 公式
    @return:技术指标的list
    """
    relist = []
    formual = formual.replace(' ', '')
    f_list = re.split('[+ * / ( ) -]', formual)

    for i in f_list:
        if i == '' or i in __mathstr or is_number(i) or i in __equalstr:
            continue
        relist.append(i)
    return relist
