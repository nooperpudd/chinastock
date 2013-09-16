# encoding:utf8


# 包含股票进步的基础数据信息
#
#
#
#
__author__ = 'nooper'
import re
import json
import cStringIO
import os

from bs4 import BeautifulSoup

from httpGet import httpGetContent
from common import decimal, validate_decimal, str_to_date





#todo  正常可以用
def stock_base_code():
    """
    根据同花顺股票列表数据，得到股票信息
    code: 600383
    name :金地集团
    market： sh,sz
    sh:上证股票
    sz:深证股票
    """
    file = os.path.dirname(__file__) + '/code.txt'
    regex = re.compile('(\d{6})')
    f = open(file, 'r')
    lines = f.readlines()
    for line in lines:
        line = line.strip('\n')
        if line != '':
            p = line.decode('GBK').encode('utf8')
            market = p[:2]
            code = re.findall(regex, p)[0]
            name = p.split('\t')[1].strip('\t')
            yield (code, name, market)
    f.close()


# todo 正常可用
def stock_finical_quarter(code):
    """
    通过同花顺行业数据得到数据报告信息。
    指标\日期	  基本每股收益	摊薄每股收益	每股净资产	每股现金流	每股未分配利润	每股公积金	主营收入	 利润总额	     净利润	 净资产收益率	销售毛利率	主营收入同比增长率	净利润同比增长率
    2013-3-31	0.04	      0.04	       5.33	      -0.68	       2.66	          1.37	    425230.9 37821.37	18722.95	0.79	26.43	143.93	19.68
    http://basic.10jqka.com.cn/600383/xls/Important_declaredate.xls"
    """
    url = "http://basic.10jqka.com.cn/%s/xls/Important_declaredate.xls" % (code)
    content = httpGetContent(url)
    stock_dict = {}
    if content:
        content = content.decode('gb2312').encode('utf8')
        data = cStringIO.StringIO(content)
        for i, line in enumerate(data):
            if i == 1:
                item = line.strip('\n').split('\t')
                date = str_to_date(item[0], "%Y-%m-%d")   # 日期
                earnings = decimal(item[2])               # 摊薄每股收益（数据相对准确）不以基本每股收益为准 0.04
                net_asset_value = decimal(item[3])        # 每股净资产 5.33
                cash_flow = decimal(item[4])              # 每股现金流 -0.86
                profit_per_share = decimal(item[5])       # 每股未分配利润
                capital_fund = decimal(item[6])           # 每股公积金
                main_income = decimal(item[7])            # 主营业收入
                total_profit = decimal(item[8])           # 利润总额
                total_net_profit = decimal(item[9])       # 净利润
                return_on_asserts = decimal(item[10])     # 净资产收益率 0.79%
                income_rise = decimal(item[12])           # 主营业收入同比增长率 143.93%
                net_profit_rise = decimal(item[13])       # 净利润同比增长率 19.68%
                stock_dict = {
                    "code": code,
                    "date": date,
                    "earnings": earnings,
                    "net_asset_value": net_asset_value,
                    "cash_flow": cash_flow,
                    "return_on_asserts": return_on_asserts,
                    "income_rise": income_rise,
                    "net_profit_rise": net_profit_rise,
                    "profit_per_share": profit_per_share,
                    "capital_fund": capital_fund,
                    "main_income": main_income,
                    "total_profit": total_profit,
                    "total_net_profit": total_net_profit
                }
                break
    return stock_dict


def stock_base_info(code):
    """
    得到股票其他的基础数据信息
    包含：
    pe_trands 市盈率（动态）：47.98
    type 分类 ：big（大盘股）medium （中盘股）small（小盘股）
    pe_static 市盈率（静态）：8.61
    total_capital 总股本 44.7亿股
    ciculate_capital 流通股本 44.7亿股
    pb 市净率 1.24

    """
    url = "http://basic.10jqka.com.cn/%s/" % code
    content = httpGetContent(url)
    if content:
        stock_dict = {}
        soup = BeautifulSoup(content)
        profile = soup.select('div#profile')
        table = profile[0].select('table')[1]
        td_list = table.select('td')
        td_select = lambda td: td.select('span')[1].text
        # regex = re.compile(r'^([0-9]{1,}[.][0-9]*|-[0-9]{1,}[.][0-9]*|\d+|-\d+)')
        # find = lambda value: float(re.findall(regex, value)[0]) if re.findall(regex, value) else None
        stock_dict["code"] = code
        for i, td in enumerate(td_list):
            if i == 0:    # 市盈率(动态)：
                stock_dict["pe_ratio_dynamic"] = validate_decimal(td_select(td))
            elif i == 3:  # 分类
                text = td_select(td)
                if text == u"大盘股":
                    stock_dict['type'] = 'big'
                elif text == u'中盘股':
                    stock_dict['type'] = 'medium'
                elif text == u"小盘股":
                    stock_dict['type'] = 'small'
                else:
                    stock_dict['type'] = text
            elif i == 4:  # 市盈率(静态)
                stock_dict['pe_ratio_static'] = validate_decimal(td_select(td))
            elif i == 7:  # 总股本
                stock_dict['total_capital'] = validate_decimal(td_select(td))
            elif i == 8:  # 市净率
                stock_dict['pb'] = validate_decimal(td_select(td))
            elif i == 11: # 流通股本
                stock_dict['circulate_capital'] = validate_decimal(td_select(td))
        return stock_dict


#todo 数据分析有问题
# def getStockFinicalAdvPost():
#     """抓取同花顺业绩预告分析板块
#     http://data.10jqka.com.cn/interface/financial/yjyg/enddate/desc/4/null/0/2013-06-30
#     """
#     headers = {
#         "Host": "data.10jqka.com.cn",
#         "Referer": "http://data.10jqka.com.cn/financial/yjyg/",
#         "X-Requested-With": "XMLHttpRequest"
#     }
#     number = range(1, 50)
#     urls = ["http://data.10jqka.com.cn/interface/financial/yjyg/enddate/desc/%s/null/0/2013-06-30" % num for num in
#             number]
#     for url in urls:
#         content = httpGetContent(url, headers)
#         if content:
#             jsoncontent = json.loads(content)
#             stock_list = jsoncontent["data"]
#             if not stock_list:
#                 continue
#             for stock in stock_list:
#                 stock_dict = {}
#                 stock_dict["postdate"] = stock["enddate"] #公告日期
#                 stock_dict["date"] = stock["rdate"] #报表日期
#                 stock_dict["code"] = stock["stockcode"] #日期
#                 stock_dict["per_eps"] = float(stock["mgsytqb"]) #每股收益
#                 stock_dict["profit_percent"] = float(stock["jlrbdfd"]) #净利润变动幅度
#                 stock_dict["increase_type"] = stock["yglx"] #预告类型
#                 stock_dict["content"] = stock["ygzy"] #预告摘要
#                 stock_dict["type"] = stock["datename"] #中报
#                 yield stock_dict


# def getStockFinicalPerPost():
#     """
#     抓取同花顺业绩快报板块
#     http://data.10jqka.com.cn/financial/yjkb/
#     """
#     headers = {
#         "Host": "data.10jqka.com.cn",
#         "Referer": "http://data.10jqka.com.cn/financial/yjkb/",
#         "X-Requested-With": "XMLHttpRequest"
#     }
#     count = range(1, 50)
#     urls = ["http://data.10jqka.com.cn/interface/financial/yjkb/rdate/desc/%s/null/2013-06-30" % num for num in count]
#     for url in urls:
#         content = httpGetContent(url, headers)
#         if content:
#             jsoncontent = json.loads(content)
#             stock_list = jsoncontent["data"]
#             if not stock_list:
#                 continue
#             for stock in stock_list:
#                 stock_dict = {}
#                 stock_dict["code"] = stock["stockcode"]
#                 stock_dict["postdate"] = stock["rdate"] #公告日期
#                 stock_dict["per_eps"] = float(stock["mgsy"]) #每股收益
#                 stock_dict["asset_increase_percent"] = __convertfloat(stock["jlrtqb"]) #净利润同比增长
#                 stock_dict["income_increase_percent"] = __convertfloat(stock["yysrtqb"]) #营业额收入同比增长
#                 stock_dict["assets_percent"] = __convertfloat(stock["zcsyl"]) #资产收益率 百分比
#                 stock_dict["income_total"] = __convertfloat(stock["yysr"]) #营业收入百万元
#                 stock_dict["net_profit"] = __convertfloat(stock["jlr"]) #净利润收入，百万元
#                 stock_dict["post_type"] = stock["datename"] #预告类型
#                 yield stock_dict






def stock_finical_post():
    """抓取同花顺业绩公告板块
    http://data.10jqka.com.cn/financial/yjgg/
    http://data.10jqka.com.cn/financial/yjgg/page/56/ajax/1/
    """
    headers = {
        "Host": "data.10jqka.com.cn",
        "Referer": "http://data.10jqka.com.cn/financial/yjyg/",
        "X-Requested-With": "XMLHttpRequest"
    }
    count = range(1, 60)
    urls = ["http://data.10jqka.com.cn/financial/yjgg/page/%s/ajax/1/" % num for num in count]
    for url in urls:
        content = httpGetContent(url, headers, "gb2312")
        if content:
            soup = BeautifulSoup(content)
            stock_item = soup.select("tbody > tr")
            for item in stock_item:
                tds = item.select('td')
                stock_dict = {}
                for i, td in enumerate(tds):
                    if i == 1:   # 代码
                        stock_dict["code"] = td.select('a')[0].string
                    elif i == 3: # 日期
                        stock_dict["date"] = str_to_date(td.string, "%Y-%m-%d")
                    elif i == 4: # 每股收益
                        stock_dict["earnings"] = decimal(td.string)
                    elif i == 5: # 营业收入
                        stock_dict["main_income"] = decimal(td.string)
                    elif i == 6: # 营业收入同比增长%
                        stock_dict["income_rise"] = validate_decimal(td.string)
                    elif i == 7: # 净利润 万元
                        stock_dict["net_profit"] = decimal(td.string)
                    elif i == 8: #净利润同比增长%
                        stock_dict["net_profit_rise"] = validate_decimal(td.string)
                yield stock_dict


#todo 测试完成
def stock_industry():
    """
    @注意该股票会包含部分st股票，但是实际选股票数据不会包含st股票数据
    得到股票的板块历史数据信息
    http://q.10jqka.com.cn/stock/thshy/
    http://q.10jqka.com.cn/interface/stock/thshy/zdf/desc/1/quote/quote
    """
    url = ('http://q.10jqka.com.cn/interface/stock/thshy/zdf/desc/1/quote/quote',
           'http://q.10jqka.com.cn/interface/stock/thshy/zdf/desc/2/quote/quote')
    for u in url:
        content = httpGetContent(u)
        if content:
            json_stock = json.loads(content)
            industry_list = json_stock['data']
            for industry in industry_list:
                num = int(industry['num'])
                industry_str = industry['hycode']

                industry_dict = {}
                industry_dict['industry_id'] = industry['platecode']
                industry_dict['industry_str'] = industry_str
                industry_dict['name'] = industry['platename']
                industry_dict['num'] = num

                #/用于处理判定数量的请求信息
                if num / 50 >= 1:
                    url_no = [n for n in range(1, num / 50 + 2)]
                elif num / 50 == 0 or num == 50:
                    url_no = [1]
                industry_url_list = ['http://q.10jqka.com.cn/interface/stock/detail/zdf/desc/%s/1/%s' \
                                     % (i, industry_str) for i in url_no]
                code_list = []
                for industry_url in industry_url_list:
                    industry_content = httpGetContent(industry_url)
                    if industry_content:
                        stock_dict = json.loads(industry_content)
                        stock_list = stock_dict['data']
                        for n in stock_list:
                            code_list.append(n['stockcode'])
                industry_dict['stock'] = code_list
                yield industry_dict



def stock_industry_day():
    """
    根据同花顺得到板块数据分析
    http://q.10jqka.com.cn/stock/thshy/
    http://q.10jqka.com.cn/interface/stock/thshy/zdf/desc/1/quote/quote
    """
    urls = ('http://q.10jqka.com.cn/interface/stock/thshy/zdf/desc/1/quote/quote',
            'http://q.10jqka.com.cn/interface/stock/thshy/zdf/desc/2/quote/quote')
    for url in urls:
        content = httpGetContent(url)
        if content:
            json_stock = json.loads(content)
            industry_list = json_stock["data"]

            for industry in industry_list:
                industry_dict = {}
                industry_dict["date"] = str_to_date( json_stock["rtime"][:10],"%Y-%m-%d")
                industry_dict["name"] = industry["platename"]
                industry_dict["industry_code"] = industry["platecode"]
                industry_dict["price"] = float(industry["zxj"])        # 最近价格
                industry_dict["volume"] = float(industry["cjl"])       # 总成交量多少万手
                industry_dict["total"] = float(industry["cje"])        # 总成交额多少亿元数据
                industry_dict["rise_percent"] = float(industry["zdf"]) # 涨跌幅
                industry_dict["rise_price"] = float(industry["zde"])   # 涨跌额度（价格）
                industry_dict["net_inflow"] = float(industry["jlr"])   # 净流入（亿元数据）
                yield industry_dict






if __name__ == "__main__":
    pass