# -*- coding: utf-8 -*-
__author__ = 'vivian'

import unittest
from dss_python_sdk.queue_utils import get_queue_properties


class TestDBUtils(unittest.TestCase):
    def test_get_queue_properties(self):
        url = "https://test.example.com/dss/queue"
        plat_key = "xx"
        svc_code = "xx"
        profile = "xx"
        user_agent = svc_code
        queues = get_queue_properties(url, plat_key, svc_code, profile, user_agent)
        for (k, v) in queues.items():
            print("mq-n:%s, ip:%s, port:%d, vhost:%s, username:%s, password:%s" %
                  (k, v["ip"], v["port"], v["vhost"], v["username"], v["password"]))
