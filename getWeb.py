#! /usr/bin/env python
# encoding:utf-8
__author__ = 'nooper'
import urllib2
import gzip
import cStringIO
import zlib
import httplib2


# def GetContent(url, gzip=False, charset=None, headers=None):
#     "用于解析url内容"
#     try:
#         msg = None
#         if headers:
#             request = urllib2.Request(url=url, headers=headers)
#         else:
#             request = urllib2.Request(url)
#         content = urllib2.urlopen(request)
#         if content.msg == 'OK' and content.getcode() == 200:
#             encoding = content.headers.get('content-encoding', None)
#             if encoding in ['gzip', 'deflate']:
#                 if encoding == 'gzip':
#                     msg = GzipStream(content)
#                 elif encoding == 'deflate':
#                     msg = zlib.decompress(content).read()
#             else:
#                 msg = content.read()
#             if charset:
#                 return msg.decode(charset).encode('utf8')
#             return msg
#     except Exception  as e:
#         print e
#     else:
#         content.close()


def httpGetContent(url, headers=None, charset=None):
    "httplib2处理请求"
    try:
        http = httplib2.Http()
        request, content = http.request(uri=url, headers=headers)
        if request.status == 200 and content:
            if charset:
                return content.decode(charset).encode('utf8')
            else:
                return content
    except Exception as e:
        raise e


def GzipStream(streams):
    "用于处理容启动gzip压缩"
    if streams:
        data = cStringIO.StringIO(streams)
        g = gzip.GzipFile('', 'rb', 9, data)
        return g.read()
        