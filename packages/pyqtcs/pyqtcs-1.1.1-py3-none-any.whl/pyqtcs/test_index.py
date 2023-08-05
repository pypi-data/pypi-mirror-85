# -*- coding:utf-8 -*-
import numpy as np
import pyqtcs

a = [1, 2, 3.9, 4, 5, 6, 7, 8, 9, 0, 2, 6, 2, 4, 6, 8, 1, 5, 3, 9, 0, 2, 4, 6, 8, 3, 5, 4, 2, 7, 5]
s = np.array(a)
print(' 原始值 ', s)
print(' boll 下值 ', pyqtcs.BOLL(s, 4, 2)[2])

# MA5 = np.array(a)
MA5 = a

b = [0, 2, 4, 6, 8, 3, 5, 4, 2, 7, 5, 334, 6, 78, 9]
MA6 = np.array(b)
# MA6 = b

s_str = '1+4*np.sin(MA5)/12+np.cos(MA6)'
s = '1+4*sin(5)/12'
names = locals()

print(' 解析后 ', pyqtcs.get_split_index(s_str))
print(' 单值计算 1 ', pyqtcs.calc_formula(s))
print(' 单值计算 2 ', pyqtcs.calc_single_formula(s_str, names))
# print(' 给值进行序列计算  ', eval(s_str))


print(' 不给值序列计算 ', pyqtcs.calc_series_formula(s_str, names))
