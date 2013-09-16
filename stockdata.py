# encoding: utf8

#部分网站api数据有bug，这个bug问题不是自身程序的问题，而是第三方公司股票的问题

__author__ = 'nooper'

import re
from math import ceil
import datetime

from httpGet import httpGetContent
from common import decimal


def _get_content(content):
    "处理腾讯股票数据接口信息"
    regex = re.compile(r'"(.*)"')
    result = regex.findall(content)
    if result:
        return result[0].split('~')


def getStockPosition(code, market):
    """
    处理股票盘口数据分析,分析所占的百分比率
    http://qt.gtimg.cn/q=s_pksz000858
    v_s_pksz000858="0.196~0.258~0.221~0.325";
    以 ~ 分割字符串中内容，下标从0开始，依次为：
    0: 买盘大单
    1: 买盘小单
    2: 卖盘大单
    3: 卖盘小单
    所占有的百分比百分比率
    """
    if code and market:
        url = "http://qt.gtimg.cn/q=s_pk%s%s" % (market, code)
        content = httpGetContent(url)
        if content:
            result_list = _get_content(content)
            if result_list:
                stock_dict = {}
                stock_dict["code"] = code
                stock_dict["market"] = market
                stock_dict["buy_big_percent"] = float(result_list[0])     # 买盘大单所占百分比
                stock_dict["buy_small_percent"] = float(result_list[1])   # 买盘小单所占百分比
                stock_dict["sell_big_percent"] = float(result_list[2])    # 卖盘大单所占比重
                stock_dict["sell_small_percent"] = float(result_list[3])  # 买盘小单所占比重
                stock_dict["date"] = datetime.date.today()
                return stock_dict


# todo 数据对不上
def getStockCashFlow(code, market):
    """得到股票是资金流入流出
    http://qt.gtimg.cn/q=ff_sz000858
    v_ff_sz000858="sz000858~41773.67~48096.67~-6322.99~-5.53~10200.89~14351.02~-4150.13~-3.63~114422.25~53015.90~59770.57~五 粮 液~20121221";
    以 ~ 分割字符串中内容，下标从0开始，依次为：
     0: 代码
     1: 主力流入
     2: 主力流出
     3: 主力净流入
     4: 主力净流入/资金流入流出总和
     5: 散户流入
     6: 散户流出
     7: 散户净流入
     8: 散户净流入/资金流入流出总和
     9: 资金流入流出总和1+2+5+6
    10: 未知
    11: 未知
    12: 名字
    13: 日期
    """
    if code and market:
        url = "http://qt.gtimg.cn/q=ff_%s%s" % (market, code)
        content = httpGetContent(url)
        if content:
            result_list = _get_content(content)
            if result_list:
                stock_dict = {}
                stock_dict["code"] = code
                stock_dict["main_inflow"] = float(result_list[1])   # 主力流入
                stock_dict["main_outflow"] = float(result_list[2])  # 主力流出
                stock_dict["main_netflow"] = float(result_list[3])  # 主力净流入

                stock_dict["small_inflow"] = float(result_list[5])  # 散户流入
                stock_dict["small_outflow"] = float(result_list[6]) # 散户流出
                stock_dict["small_netflow"] = float(result_list[7]) # 散户净流入

                income = stock_dict["main_inflow"] + stock_dict["small_inflow"]
                outcome = stock_dict["main_outflow"] + stock_dict["main_outflow"]
                print income
                print outcome
                print income - outcome

                stock_dict["unknown_1"] = float(result_list[10])
                stock_dict["unknwon_2"] = float(result_list[11])
                stock_dict["date"] = result_list[13]                # 日期

                return stock_dict


def getStockCurrentDay(code, Market):
    '''
    获取股票当日数据
    腾讯API
    API地址：http://qt.gtimg.cn/q=sh600383
    sh:上海
    sz:深圳
    返回当天成交数据
    code:股票代码
    market：股票市场
    数据返回@return dict
    '''
    if code and Market:
        url = 'http://qt.gtimg.cn/q=%s%s' % (Market, code)
        headers = {'Content-type': 'application/x-javascript; charset=GBK'}
        result = httpGetContent(url=url, headers=headers, charset='gbk')
        if result:
            stocklist = _get_content(result)
            if stocklist:
                stockdict = {}
                stockdict['code'] = code                           # 股票代码
                stockdict['name'] = unicode(stocklist[1], 'utf8')  # 股票名称
                stockdict['last_closing'] = float(stocklist[4])    # 昨日收盘价格
                stockdict['start'] = float(stocklist[5])           # 开盘价格
                stockdict['end'] = float(stocklist[3])             # 当前收盘价格（可以是当前价格）
                stockdict['high'] = float(stocklist[33])           # 最高价格
                stockdict['low'] = float(stocklist[34])            # 最低价格
                stockdict['buyvol'] = int(stocklist[7])             # 外盘 todo 数据对不上
                stockdict["sellvol"] = int(stocklist[8])           # 内盘 todo 数据对不上

                stockdict['range_price'] = float(stocklist[31])    # 涨跌价格
                stockdict['range_percent'] = float(stocklist[32])  # 涨跌比%

                stockdict['volume'] = int(stocklist[6])            # 成交量（手）
                stockdict['total_price'] = int(stocklist[37])      # 成交额（万元）
                stockdict['change_rate'] = decimal(stocklist[38]) # 换手率
                stockdict['pe'] = decimal(stocklist[39])          # 市盈率
                stockdict['swing'] = float(stocklist[43])           # 振幅

                stockdict['pb'] = float(stocklist[46])              # 股票市净率
                stockdict['date'] = stocklist[30][:8]               # 时间
                stockdict["block"] = False if stockdict["start"] else True #股票是否停牌
                return stockdict


def getStockMarket(code):
    """
    大盘数据接口信息
    上证：code:000001 set=zs
    深证：code:399001 set=zs
    中小板：code:399005 set=zs
    创业板: code:399006 set=zs
    http://q.stock.sohu.com/qp/hq?type=snapshot&code=000001&set=zs

    """
    url = "http://q.stock.sohu.com/qp/hq?type=snapshot&code=%s&set=zs" % code

    result = httpGetContent(url=url, charset="gbk")
    if result:
        result = eval(result)
        stock_dict = {}
        stock_dict["date"] = result[0][:10] #日期
        stock_dict["name"] = unicode(result[2], 'utf8') #名称
        stock_dict["range_price"] = float(result[4]) #上涨价格
        stock_dict["range_percent"] = float(result[5].strip("%")) #涨幅

        stock_dict["start"] = float(result[9]) #开盘价格
        stock_dict["high"] = float(result[11]) #最高价格
        stock_dict["low"] = float(result[13]) #最低价格
        stock_dict["last_closing"] = float(result[7]) #昨日收
        stock_dict["end"] = float(result[3]) #收盘价格

        stock_dict["total_sum"] = int(result[18]) #多少万元

        stock_dict["volume"] = int(result[14]) #多少手

        return stock_dict


tonghuashun_headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip,deflate,sdch",
    "Accept-Language": "zh-CN,zh;q=0.8",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Host": "qd.10jqka.com.cn",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36"
}

# def getstockBlock():
#     """
#     新浪股票黑名单数据
#     ”需要得到单点登录信息“
#
#     新浪股票黑名单个股
#     http://weibo.gxq.com.cn/stock/disallowStock
#     """
#     headers = {
#         'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#         'Cache-Control': "max-age=0",
#         'Host': 'weibo.gxq.com.cn',
#         'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36',
#         'Cookie': "PHPSESSID=c32fbi3m3sf0he8v1rdem3t006; gxqSignId=02d9c361fe5fc1ab; WBStore=d6acd6adea5a82d3|undefined"
#
#     }
#     url = "http://weibo.gxq.com.cn/stock/disallowStock"
#     content = httpGetContent(url=url, headers=headers)
#     if content:
#         soup = BeautifulSoup(content)
#         td_list = soup.find_all(text=re.compile('\d+'))
#         return td_list


def __convert_MIN(content):
    content = content.split('=')[1]
    content_list = content.split('|')
    stock_dict = {}
    for sub in content_list:
        if sub:
            items = sub.split('~')
            date = items[0]
            price_list = items[1].split(';')
            price_dict = {}
            for a in price_list:
                b = a.split(',')
                start = float(b[0]) #开盘价
                high = float(b[1]) #最高价格
                low = float(b[2]) #最低价格
                end = float(b[3]) #结束价格
                volum = int(ceil(float(b[4]))) #成交量多少买入
                total_price = int(ceil(float(b[5]))) #成交额
                time = b[6] #时间格式是1030，11：30，1400，1500

                price_dict[time] = {
                    "high": high,
                    'low': low,
                    "end": end,
                    "start": start,
                    "volumn": volum,
                    "total_price": total_price
                }
            stock_dict[date] = price_dict
    return stock_dict


def getStock60MIN(code, market, type=''):
    """
    不推荐向后复权
    得到股票60分钟数据线
    API接口数据
    http://qd.10jqka.com.cn/api.php?p=stock_min60&info=k_sz_000005&fq=q
    q是向前复权
    b事项后复权
    q= 空是不复权
    """
    if market not in ('sz', 'sh'):
        return

    url = "http://qd.10jqka.com.cn/api.php?p=stock_min60&info=k_%s_%s&fq=%s" % (market, code, type)

    content = httpGetContent(url=url)
    if content:
        return __convert_MIN(content)


def getStock30MIN(code, market, type=''):
    """
    30分钟数据接口信息
    http://qd.10jqka.com.cn/api.php?p=stock_min30&info=k_sz_000005&fq=
    """
    if market not in ('sz', 'sh'):
        return
    url = "http://qd.10jqka.com.cn/api.php?p=stock_min30&info=k_%s_%s&fq=%s" % (market, code, type)
    content = httpGetContent(url=url)
    if content:
        return __convert_MIN(content)


def getStock15MIN(code, market, type=''):
    """
    15分钟数据接口
    http://qd.10jqka.com.cn/api.php?p=stock_min15&info=k_sz_000005&fq=
    """
    if market not in ('sz', 'sh'):
        return
    url = "http://qd.10jqka.com.cn/api.php?p=stock_min15&info=k_%s_%s&fq=%s" % (market, code, type)
    content = httpGetContent(url=url)
    if content:
        return __convert_MIN(content)


def __convert_inner(stock, stock_dict={}):
    stock_day = stock.split(',')
    if all(stock_day):
        date = stock_day[0] #日期
        start = float(stock_day[1]) #开盘价格
        high = float(stock_day[2]) #最高价格
        low = float(stock_day[3]) #最低价格
        end = float(stock_day[4]) #收盘价格
        volume = int(ceil(float(stock_day[5]))) #成交量
        total = int(ceil(float(stock_day[6]))) #成交额

        stock_dict[date] = {
            "date": date,
            'start': start,
            'high': high,
            'low': low,
            'end': end,
            'volume': volume,
            'total': total,
        }
        return stock_dict


def __convert_day(content):
    stock_list = content.split('=')[1].split('|')
    stock_dict = {}
    for stock in stock_list:
        if stock and stock.strip():
            __convert_inner(stock, stock_dict)
            # stock_day = stock.split(',')
            # date = stock_day[0] #日期
            # start = stock_day[1] #开盘价格
            # high = stock_day[2] #最高价格
            # low = stock_day[3] #最低价格
            # end = stock_day[4] #收盘价格
            # volume = int(ceil(float(stock_day[5]))) #成交量
            # total = int(ceil(float(stock_day[6]))) #成交额
            # stock_dict[date] = {
            #         "date": date,
            #         'start': start,
            #         'high': high,
            #         'low': low,
            #         'end': end,
            #         'volume': volume,
            #         'total': total,
            #     }
    return stock_dict


def __convert_week(content):
    content_list = content.split(';')
    regex = re.compile('=(.*)$')
    stock_dict = {}
    for s in content_list:
        p = regex.findall(s)[0]
        stock_list = p.split('|')
        for week in stock_list:
            if week:
                __convert_inner(week, stock_dict)

    return stock_dict

#todo 测试完成
def getStockDayHistory(code, market, year='2013', type=''):
    """
    http://qd.10jqka.com.cn/api.php?p=stock_day&info=k_sz_000005&year=2012,2013&fq=
    sz:深证
    sh:上海
    return dict
    """
    url = "http://qd.10jqka.com.cn/api.php?p=stock_day&info=k_%s_%s&year=%s&fq=%s" % (market, code, year, type)
    content = httpGetContent(url=url)
    if content:
        return __convert_day(content)

#todo 测试完成
def getStockWeekHistory(code, market, year='2012,2013', type=''):
    """
    xhttp://qd.10jqka.com.cn/api.php?p=stock_week&info=k_sz_000005&year=2011,2012,2013&fq=
    pass
    """
    url = "http://qd.10jqka.com.cn/api.php?p=stock_week&info=k_%s_%s&year=%s&fq=%s" % (market, code, year, type )
    content = httpGetContent(url, tonghuashun_headers)
    if content:
        return __convert_week(content)


def __convertMonth(content):
    pass


def getStockMonthHistory(code, market, type=''):
    """
    http://qd.10jqka.com.cn/api.php?p=stock_month&info=k_sz_000671&fq=
    """
    url = "http://qd.10jqka.com.cn/api.php?p=stock_month&info=k_%s_%s&fq=%s" % (market, code, type)
    content = httpGetContent(url)
    if content:
        pass


def main():
    # g = getStock60MIN('600847', 'sh')
    # for k in g:
    #     print k
    #     print g[k]
    # g = getStockDayHistory("600198", "sh")
    # print g

    # import config
    #
    # print getStockMarket(config.SHANGHAI)
    print getStockCurrentDay("600383", "sh")


if __name__ == "__main__":
    main()