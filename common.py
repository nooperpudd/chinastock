# encoding:utf-8
__author__ = 'nooper'

import re
from datetime import datetime


def str_to_date(date_str, format="%Y%m%d"):
    """
    将字符串转换成时间函数
    """
    return datetime.strptime(date_str, format)

def validate_decimal(value):
    """
    验证小数数据
    """
    if value:
        regex = re.compile(r'^([0-9]{1,}[.][0-9]*|-[0-9]{1,}[.][0-9]*|\d+|-\d+)')
        value = re.findall(regex, value)[0]
        return decimal(value)


def decimal(value):
    try:
        if value and value != "":
            return float(value)
    except Exception as e:
        return 0.0