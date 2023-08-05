# -*- coding: utf-8 -*-
__author__ = 'vivian'
import sys


def http_get(url, user_agent, prams, time_out):
    """
    http get request,
    :param url:
    :param user_agent:
    :param prams:
    :param time_out:
    :return:
    """
    if sys.version > '3':
        import urllib3
        import urllib
        data = urllib.parse.urlencode(prams)
        url = url + "?" + data
        http = urllib3.PoolManager(timeout=time_out, cert_reqs='CERT_NONE')
        f = http.request(method='GET', url=url, headers={"User-Agent": user_agent})
        res_bytes = f.data
        msg = res_bytes.decode("utf-8")
        f.close()
        return msg
    else:
        import urllib2
        import ssl
        import urllib
        data = urllib.urlencode(prams)
        url = url + "?" + data
        request = urllib2.Request(url, headers={"User-Agent": user_agent})
        f = urllib2.urlopen(request, timeout=time_out, context=ssl._create_unverified_context())
        res_bytes = f.read()
        f.close()
        return res_bytes
