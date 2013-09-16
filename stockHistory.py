# encoding:utf8

#部分股票数据历史价格有误，尤其是2011年以前的数据，等一些历史数据
#无论是yahoo还是新浪的


__author__ = 'nooper'
import cStringIO
import csv

from bs4 import BeautifulSoup

from httpGet import httpGetContent


#年
years = ["2010", "2011", "2012", "2013"]
#季度
quarter = [1, 2, 3, 4]


def stock_day_history_sina(stock_code, year, qr):
    """
    stockcode:股票代码
    market：市场
    year：2013
    qr：季度1，2，3，4格式
    货的股票历史数据
    返回数据格式
    日期2013-03-29
    开盘：10.030
    最高：10.210
    停盘：10.130
    最低9.910
    数据量131028760
    价格：1315731584
    API:http://money.finance.sina.com.cn/corp/go.php/vMS_MarketHistory/stockid/600000.phtml?year=2013&jidu=1
    """
    #todo 没有复权价格


    url = "http://money.finance.sina.com.cn/corp/go.php/vMS_MarketHistory/stockid/%s.phtml?year=%s&jidu=%s" \
          % (stock_code, year, qr)
    content = httpGetContent(url=url)
    if content:
        soap = BeautifulSoup(content)
        table = soap.select('table#FundHoldSharesTable>tbody')
        if table:
            tr_list = table[0].select('tr')
            for i, tr in enumerate(tr_list):
                stock = {}
                if i == 0 or i == 1:
                    continue
                td_list = tr.select('td')

                for j, td in enumerate(td_list):
                    if j == 0: #日期
                        stock['date'] = td.div.a.text
                    elif j == 1: #开盘价格
                        stock['start'] = float(td.div.text)
                    elif j == 2: #
                        stock['high'] = float(td.div.text)
                    elif j == 3:
                        stock['end'] = float(td.div.text)
                    elif j == 4:
                        stock['low'] = float(td.div.text)
                    elif j == 5:
                        stock['rate'] = int(round(int(td.div.text) / 100.0, 0))
                    elif j == 6:
                        stock['money'] = int(round(int(td.div.text) / 10000.0, 0))
                yield stock


# todo 完成测试
def stock_day_history_Yahoo(code, market):
    """
    雅虎股票数据接口
    得到yahoo股票的历史数据信息
    深市数据链接：http://table.finance.yahoo.com/table.csv?s=000001.sz
    上市数据链接：http://table.finance.yahoo.com/table.csv?s=600000.ss
    Date 日期
    Open 开盘价格
    High 最高价格
    Low  最低价格
    Close 结束价格
    Volume 量
    Adj Close 收盘加权价格
    """
    if market not in ('sz', 'ss'):
        return
    url = "http://table.finance.yahoo.com/table.csv?s=%s.%s" % (code, market)
    content = httpGetContent(url=url)
    if content:
        data = cStringIO.StringIO(content)
        reader = csv.reader(data)
        for i, row in enumerate(reader):
            stock_dict = {}
            if i == 0:
                continue
            stock_dict['date'] = row[0]             # 日期
            stock_dict['open'] = float(row[1])      # 开盘价格
            stock_dict['high'] = float(row[2])      # 最高价格
            stock_dict['low'] = float(row[3])       # 最低价格
            stock_dict['close'] = float(row[4])     # 结束价格
            stock_dict['volume'] = float(row[5])    # 量
            stock_dict['adj_close'] = float(row[6]) # 几日收盘加权价格？
            yield stock_dict


def main():
    pass
    # code = getStockDayHistoryByYahoo('601989', 'ss')
    # for cod in code:
    #     print cod


if __name__ == "__main__":
    main()