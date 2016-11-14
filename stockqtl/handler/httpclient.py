# encoding:utf-8

import requests


def request(url, method="get", header=None, params=None):
    """
    :param url:
    :param header:
    :return:
    """

    response = requests.request(method=method, url=url, header=header, params=params)
    if response.status_code == 200:
        content = response.content
        return content
    else:
        raise Exception("no data")
