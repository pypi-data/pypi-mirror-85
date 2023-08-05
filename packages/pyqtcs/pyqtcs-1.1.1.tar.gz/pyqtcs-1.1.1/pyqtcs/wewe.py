# -*- coding:utf-8 -*-
from numba import jit

import pyqtcs
import numpy as np
import numba
import QuantLib as ql
import timeit

print(pyqtcs.__version__)

pyqtcs.qtclass.print_test()

a = np.array([1, 23, 45, 6, 78, 9])
print(pyqtcs.MA(a, 2))

f = '1+3+4'
print(pyqtcs.calc_formula(f))

print(ql.__version__)
