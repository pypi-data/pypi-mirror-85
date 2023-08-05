# -*- coding:utf-8 -*-

from __future__ import division
import pyparsing as pyp
import numpy as np
import operator

import sys

from pyqtcs.func.split_index import get_split_index


class __formula_analysis(object):

    def pushFirst(self, strg, loc, toks):
        self.exprStack.append(toks[0])

    def pushUMinus(self, strg, loc, toks):
        if toks and toks[0] == '-':
            self.exprStack.append('unary -')

    def __init__(self):
        """
        expop   :: '^'
        multop  :: '*' | '/'
        addop   :: '+' | '-'
        integer :: ['+' | '-'] '0'..'9'+
        atom    :: PI | E | real | fn '(' expr ')' | '(' expr ')'
        factor  :: atom [ expop factor ]*
        term    :: factor [ multop factor ]*
        expr    :: term [ addop term ]*
        """
        point = pyp.Literal(".")
        e = pyp.CaselessLiteral("E")
        fnumber = pyp.Combine(pyp.Word("+-" + pyp.nums, pyp.nums) +
                              pyp.Optional(point + pyp.Optional(pyp.Word(pyp.nums))) +
                              pyp.Optional(e + pyp.Word("+-" + pyp.nums, pyp.nums)))
        ident = pyp.Word(pyp.alphas, pyp.alphas + pyp.nums + "_$")
        plus = pyp.Literal("+")
        minus = pyp.Literal("-")
        mult = pyp.Literal("*")
        div = pyp.Literal("/")
        lpar = pyp.Literal("(").suppress()
        rpar = pyp.Literal(")").suppress()
        addop = plus | minus
        multop = mult | div
        expop = pyp.Literal("^")
        pi = pyp.CaselessLiteral("PI")
        expr = pyp.Forward()
        atom = ((pyp.Optional(pyp.oneOf("- +")) +
                 (pi | e | fnumber | ident + lpar + expr + rpar).setParseAction(self.pushFirst))
                | pyp.Optional(pyp.oneOf("- +")) + pyp.Group(lpar + expr + rpar)
                ).setParseAction(self.pushUMinus)
        # by defining exponentiation as "atom [ ^ factor ]..." instead of
        # "atom [ ^ atom ]...", we get right-to-left exponents, instead of left-to-right
        # that is, 2^3^2 = 2^(3^2), not (2^3)^2.
        factor = pyp.Forward()
        factor << atom + pyp.ZeroOrMore((expop + factor).setParseAction(
            self.pushFirst))
        term = factor + pyp.ZeroOrMore((multop + factor).setParseAction(
            self.pushFirst))
        expr << term + pyp.ZeroOrMore((addop + term).setParseAction(self.pushFirst))
        self.bnf = expr
        # map operator symbols to corresponding arithmetic operations
        epsilon = 1e-12
        self.opn = {"+": operator.add,
                    "-": operator.sub,
                    "*": operator.mul,
                    "/": operator.truediv,
                    "^": operator.pow}
        self.fn = {"sin": np.sin,
                   "cos": np.cos,
                   "tan": np.tan,
                   "abs": abs,
                   "trunc": lambda a: int(a),
                   "round": round,
                   "sgn": lambda a: abs(a) > epsilon and cmp(a, 0) or 0}
        self.exprStack = []

    def evaluateStack(self, s):
        op = s.pop()
        if op == 'unary -':
            return -self.evaluateStack(s)
        if op in "+-*/^":
            op2 = self.evaluateStack(s)
            op1 = self.evaluateStack(s)
            return self.opn[op](op1, op2)
        elif op == "PI":
            return np.pi  # 3.1415926535
        elif op == "E":
            return np.e  # 2.718281828
        elif op in self.fn:
            return self.fn[op](self.evaluateStack(s))
        elif op[0].isalpha():
            return 0
        else:
            return float(op)

    def eval(self, num_string, parseAll=True):
        self.exprStack = []
        self.bnf.parseString(num_string, parseAll)
        val = self.evaluateStack(self.exprStack[:])
        return val


__nsp = __formula_analysis()


def calc_formula(string_formula):
    """
    通过计算公式计算值
    :param string_formula:
    :return:
    """

    return __nsp.eval(string_formula)


def calc_single_formula(string_formula, dict_values):
    """
    通过计算公式计算值
    @param string_formula:
    @param dict_values:
    """
    spilt_index = get_split_index(string_formula)
    for item in spilt_index:
        tempvalue = dict_values[item][-1]
        exec('{} = {}'.format(item, tempvalue))

    return eval(string_formula)


def calc_series_formula(string_formula, dict_values):
    """
    按照公式，计算序列值
    @param string_formula: 公式
    @param dict_values: 值对象dict
    @return: 计算后的序列值
    """
    spilt_index = get_split_index(string_formula)

    # 获取最小长度值
    min_count = sys.maxsize
    for item in spilt_index:
        count = len(dict_values[item])
        if count < min_count:
            min_count = count

    # 对每个给定值进行按最小长度值排序，对于长的，需要从后面截取数值
    for item in spilt_index:
        tempvalue = dict_values[item]
        if type(tempvalue) is list:
            tempvalue = tempvalue[len(tempvalue) - min_count:]
        elif type(tempvalue) is np.ndarray:
            tempvalue = tempvalue[len(tempvalue) - min_count:].tolist()

        exec('{} = {}'.format(item, tempvalue))

    return eval(string_formula)
