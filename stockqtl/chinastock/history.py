# encoding:utf-8

from dateutil import parser

def get_stock_history(code, start_date,end_date=None,date_type="day",data_type=""):
    """
    得到股票历史行情数据

    date_type: day, week, month
    day: 1day
    week: 1week,
    month: 1month

    :param code:
    :param start_date:
    :param end_date:
    :return:
    """
    url = ""
    start_date = parser.parse(start_date).date()





