# encoding:utf8
__author__ = 'nooper'
import re
import urllib2, urllib
import json
from bs4 import BeautifulSoup
from getWeb import httpGetContent
import cStringIO
import os


def __convertfloat(value):
    try:
        if value:
            return float(value)
    except:
        return 0.0



#todo  正常可以用
def getstockBase():
    """
    根据同花顺股票列表数据，得到股票信息
    “非ST股票”
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
def getStockFinical(code):
    """
    http://basic.10jqka.com.cn/600383/xls/Important_declaredate.xls"
    """
    url = "http://basic.10jqka.com.cn/%s/xls/Important_declaredate.xls" % (code)
    content = httpGetContent(url)
    stock_dict = {}
    if content:
        content = content.decode('gb2312').encode('utf8')

        data = cStringIO.StringIO(content)
        convertfloat = lambda value: float(value) if value != "" else None
        for i, line in enumerate(data):
            if i == 1:
                item = line.strip('\n').split('\t')
                date = item[0] #日期
                per_income = convertfloat(item[2])  #每股收益 0.04
                per_net_asset = convertfloat(item[3])  #每股净资产 5.33
                per_cash = convertfloat(item[4])  #每股现金流 -0.86
                net_asset_percent = convertfloat(item[10])  #净资产收益率 0.79%
                income_rise_percent = convertfloat(item[12])   #主营业收入同比增长率 143.93%
                net_profit_rise_percent = convertfloat(item[13]) #净利润同比增长率 19.68%
                stock_dict = {
                    "code": code,
                    "date": date,
                    "per_income": per_income, #每股收益
                    "per_net_asset": per_net_asset, #每股净资产
                    "per_cash": per_cash, #每股现金流
                    "net_asset_percent": net_asset_percent, #净资产收益率
                    "income_rise_percent": income_rise_percent, #主营业额收入同比增长率
                    "net_profit_rise_percent": net_profit_rise_percent #净利润同比增长率
                }
                break
    url2 = "http://basic.10jqka.com.cn/%s/" % code
    content = httpGetContent(url2)
    if content:
        soup = BeautifulSoup(content)
        profile = soup.select('div#profile')
        table = profile[0].select('table')[1]
        td_list = table.select('td')

        td_select = lambda td: td.select('span')[1].text
        regex = re.compile(r'^([0-9]{1,}[.][0-9]*|-[0-9]{1,}[.][0-9]*|\d+|-\d+)')
        find = lambda value: float(re.findall(regex, value)[0]) if re.findall(regex, value) else None
        for i, td in enumerate(td_list):
            if i == 0:#市盈率(动态)：
                stock_dict["pe_trands"] = find(td_select(td))
            elif i == 3: #分类
                text = td_select(td)
                if text == u"大盘股":
                    stock_dict['type'] = 'big'
                elif text == u'中盘股':
                    stock_dict['type'] = 'medium'
                elif text == u"小盘股":
                    stock_dict['type'] = 'small'
                else:
                    stock_dict['type'] = text
            elif i == 4:#市盈率(静态)
                stock_dict['pe_static'] = find(td_select(td))
            elif i == 7: #总股本
                stock_dict['total_capital'] = find(td_select(td))
            elif i == 8:#市净率
                stock_dict['pb'] = find(td_select(td))
            elif i == 11:#流通股本
                stock_dict['circulate_capital'] = find(td_select(td))
    return stock_dict




def getStockFinicalAdvPost():
    """抓取同花顺业绩预告分析板块
    http://data.10jqka.com.cn/interface/financial/yjyg/enddate/desc/4/null/0/2013-06-30
    """
    headers = {
        "Host": "data.10jqka.com.cn",
        "Referer": "http://data.10jqka.com.cn/financial/yjyg/",
        "X-Requested-With": "XMLHttpRequest"
    }
    number = range(1, 50)
    urls = ["http://data.10jqka.com.cn/interface/financial/yjyg/enddate/desc/%s/null/0/2013-06-30" % num for num in
            number]
    for url in urls:
        content = httpGetContent(url, headers)
        if content:
            jsoncontent = json.loads(content)
            stock_list = jsoncontent["data"]
            if not stock_list:
                continue
            for stock in stock_list:
                stock_dict = {}
                stock_dict["postdate"] = stock["enddate"] #公告日期
                stock_dict["date"] = stock["rdate"] #报表日期
                stock_dict["code"] = stock["stockcode"] #日期
                stock_dict["per_eps"] = float(stock["mgsytqb"]) #每股收益
                stock_dict["profit_percent"] = float(stock["jlrbdfd"]) #净利润变动幅度
                stock_dict["increase_type"] = stock["yglx"] #预告类型
                stock_dict["content"] = stock["ygzy"] #预告摘要
                stock_dict["type"] = stock["datename"] #中报
                yield stock_dict


def getStockFinicalPerPost():
    """
    抓取同花顺业绩快报板块
    http://data.10jqka.com.cn/financial/yjkb/
    """
    headers = {
        "Host": "data.10jqka.com.cn",
        "Referer": "http://data.10jqka.com.cn/financial/yjkb/",
        "X-Requested-With": "XMLHttpRequest"
    }
    count = range(1, 50)
    urls = ["http://data.10jqka.com.cn/interface/financial/yjkb/rdate/desc/%s/null/2013-06-30" % num for num in count]
    for url in urls:
        content = httpGetContent(url, headers)
        if content:
            jsoncontent = json.loads(content)
            stock_list = jsoncontent["data"]
            if not stock_list:
                continue
            for stock in stock_list:
                stock_dict = {}
                stock_dict["code"] = stock["stockcode"]
                stock_dict["postdate"] = stock["rdate"] #公告日期
                stock_dict["per_eps"] = float(stock["mgsy"]) #每股收益
                stock_dict["asset_increase_percent"] = __convertfloat(stock["jlrtqb"]) #净利润同比增长
                stock_dict["income_increase_percent"] = __convertfloat(stock["yysrtqb"]) #营业额收入同比增长
                stock_dict["assets_percent"] = __convertfloat(stock["zcsyl"]) #资产收益率 百分比
                stock_dict["income_total"] = __convertfloat(stock["yysr"]) #营业收入百万元
                stock_dict["net_porfit"] = __convertfloat(stock["jlr"]) #净利润收入，百万元
                stock_dict["post_type"] = stock["datename"] #预告类型
                yield stock_dict


def getStockFinicalPost():
    """抓取同花顺业绩公告板块
    http://data.10jqka.com.cn/financial/yjgg/
    http://data.10jqka.com.cn/interface/financial/yjgg/rdate/desc/2/null/2013-06-30
    """
    headers = {
        "Host": "data.10jqka.com.cn",
        "Referer": "http://data.10jqka.com.cn/financial/yjyg/",
        "X-Requested-With": "XMLHttpRequest"
    }
    count = range(1, 60)
    urls = ["http://data.10jqka.com.cn/interface/financial/yjgg/rdate/desc/%s/null/2013-06-30" % num for num in count]
    for url in urls:
        content = httpGetContent(url, headers)
        if content:
            jsoncontent = json.loads(content)
            stock_list = jsoncontent['data']
            if not stock_list:
                continue
            for stock in stock_list:
                stock_dict = {}
                stock_dict["code"] = stock["stockcode"]
                stock_dict["postdate"] = stock["rdate"] #业绩公告日期
                stock_dict["per_eps"] = float(stock["mgsy"]) #每股收益
                stock_dict["asset_percnet"] = __convertfloat(stock["tbsyl"]) #净资产收益率3.66%
                stock_dict["asset_increase_percent"] = __convertfloat(stock["jlrtqb"]) #净利润同比增长 -65.93%
                stock_dict["income_increase_percent"] = __convertfloat(stock["yysrtqb"]) #主营业收入同比增长
                stock_dict["gross_porfit"] = __convertfloat(stock["xsmll"]) # 销售毛利率
                stock_dict["income_total"] = float(stock["yysr"]) # 主营业收入，多少万元
                stock_dict["net_income"] = float(stock["jlr"]) #净利润，多少万元
                stock_dict["post_type"] = stock["datename"] #报告类型
                yield stock_dict


#todo 测试完成
def getStockIndustry():
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
            jsonstock = json.loads(content)
            industry_list = jsonstock['data']
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




#测试完成
def getStockIndustryDay():
    """根据同花顺得到板块数据分析
    http://q.10jqka.com.cn/stock/thshy/
    http://q.10jqka.com.cn/interface/stock/thshy/zdf/desc/1/quote/quote
    """
    urls = ('http://q.10jqka.com.cn/interface/stock/thshy/zdf/desc/1/quote/quote',
            'http://q.10jqka.com.cn/interface/stock/thshy/zdf/desc/2/quote/quote')
    for url in urls:
        content = httpGetContent(url)
        if content:
            jsonstock = json.loads(content)
            industry_list = jsonstock["data"]
            for industry in industry_list:
                industry_dict = {}
                industry_dict["date"] = jsonstock["rtime"]
                industry_dict["name"] = industry["platename"]
                industry_dict["industry_code"] = industry["platecode"] #
                industry_dict["price"] = float(industry["zxj"]) #最近价格
                industry_dict["volume"] = float(industry["cjl"]) #总成交量多少万手
                industry_dict["total_price"] = float(industry["cje"]) #总成交额多少亿元数据
                industry_dict["rise_percent"] = float(industry["zdf"]) #涨跌幅
                industry_dict["rise_price"] = float(industry["zde"]) #涨跌额度（价格）
                industry_dict["net_in_flow"] = float(industry["jlr"]) #净流入（亿元数据）
                yield industry_dict


def main():
    for stock in getStockFinicalPerPost():
        print stock
        # sh=getStockCode('sh')
    # print len(sh)
    # sz=getStockCode('sz')
    # print len(sz)
    # print len(sh)+len(sz)
    # print getstockInfo('600383')
    num = 0
    # # ins = set()
    # #
    # # # info=set()
    # # info = set(code for (code, name, market) in getstockBase())
    # for i, industry in enumerate(getStockIndustryDay()):
    #     print industry


    #
    #     print ins.update(industry['stock'])
    #
    #
    # # for indus in getStockIndustry():
    # #     num += indus['num']
    #
    # b = ins - info
    # print b
    # print len(b)
    # print "leng %s" % num
    # print getStockFinical('600212')


if __name__ == "__main__":
    main()