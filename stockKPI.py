# encoding:utf8


# 完全不准仅供参考
#
#
#
__author__ = 'nooper'

from xml.dom import minidom
from getWeb import httpGetContent
import warnings

def __parase_XML(content, prase=None):
    """
    用于处理解析xml数据文档
    """
    dom = minidom.parseString(content)
    root = dom.documentElement
    nodes = root.getElementsByTagName(prase)
    nodes.reverse()
    return nodes[:10]


def getStock_KDJ_30MIN(code, market):
    '''
    得到股票30分钟kdj数据线
    http://minpic.quote.stock.hexun.com/bdxml/30min/sz/000788/kdj.xml
    返回数据
    <Q dateTime="201306121500" K="0.85" D="0.7" J="1.16"/>
    http://minpic.quote.stock.hexun.com/bdxml/30min/sz/000788/kdj.xml
    kdj,macd,boll

    return:[{'k': u'0.85', 'j': u'1.1', 'd': u'0.73', 'time': u'201306121500'}]
    '''
    #todo 和讯网股票股票数据接口，可以用于获取指标数据
    if market not in ["sz", "sh"]:
        return
    url = " http://minpic.quote.stock.hexun.com/bdxml/30min/%s/%s/kdj.xml" % (market, code)
    content = httpGetContent(url=url)
    if content:
        nodes = __parase_XML(content, 'Q')
        kdj_list = []
        for node in nodes:
            kdj_list.append(
                {"time": node.getAttribute("dateTime"),
                 "k": node.getAttribute("K"),
                 "d": node.getAttribute("D"),
                 "j": node.getAttribute("J")
                }
            )
        return kdj_list



def getStock_MACD_30MIN(code, market):
    """
    得到股票30分钟macd数据线
    http://minpic.quote.stock.hexun.com/bdxml/30min/sz/000788/macd.xml
    """
    #TODO BUGS
    warnings.warn("数据不准确，需要重新修正数据，接口时间有问题。",DeprecationWarning)
    url = " http://minpic.quote.stock.hexun.com/bdxml/30min/%s/%s/macd.xml" % (market, code)
    content = httpGetContent(url)
    if content:
        nodes = __parase_XML(content, "Q")
        macd_list = []
        for node in nodes:
            macd_list.append(
                {
                    "time": node.getAttribute("dateTime"),
                    "macd": node.getAttribute("MACD"),
                    "signal": node.getAttribute("Signal"),
                    "spread": node.getAttribute("Spread")
                }
            )
        return macd_list


def getStock_OBV_30MIN(code,market):
    """
    得到30分钟obv数据线
    """
    url="http://minpic.quote.stock.hexun.com/bdxml/30min/%s/%s/obv.xml" % (market,code)
    content=httpGetContent(url=url)
    if content:
        nodes=__parase_XML(content,'Q')
        obv_list=[]
        for node in nodes:
            obv_list.append({
                "time":node.getAttribute('dateTime'),
                "obv":node.getAttribute("OBV")
            })
        return obv_list

def getStock_CCI_30MIN(code,market):
    """
    得到股票CCI数据线
    """
    url="http://minpic.quote.stock.hexun.com/bdxml/30min/%s/%s/cci.xml" % (market,code)
    content=httpGetContent(url=url)
    if content:
        nodes=__parase_XML(content,'Q')
        cci_list=[]
        for node in nodes:
            cci_list.append({
                'time':node.getAttribute('dateTime'),
                "cci":node.getAttribute('value')
            })
        return cci_list


def getStock_BOLL_30MIN(code,market):
    """
    得到股票30分钟boll数据线
    http://minpic.quote.stock.hexun.com/bdxml/30min/sz/000788/boll.xml

    """

    url="http://minpic.quote.stock.hexun.com/bdxml/30min/%s/%s/boll.xml"  % (market,code)
    content=httpGetContent(url=url)
    if content:
        nodes=__parase_XML(content,'Q')
        boll_list=[]
        for node in nodes:
            boll_list.append(
                {
                    "time":node.getAttribute("dateTime"),
                    "middle":node.getAttribute("Middle"),
                    "upper":node.getAttribute("Upper"),
                    "Lower":node.getAttribute("Lower")
                }
            )
        return boll_list

def main():
    pass

if __name__=="__main__":
    main()