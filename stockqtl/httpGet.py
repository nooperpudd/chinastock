#! /usr/bin/env python
# encoding:utf-8
__author__ = 'nooper'

import gzip
import cStringIO

import httplib2



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
        