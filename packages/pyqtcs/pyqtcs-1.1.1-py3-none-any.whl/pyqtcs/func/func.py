# -*- coding:utf-8 -*-

# 判断是否为数字
def is_number(s):
    """
    判断字符是否为数字
    :param s:
    :return:
    """
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False

