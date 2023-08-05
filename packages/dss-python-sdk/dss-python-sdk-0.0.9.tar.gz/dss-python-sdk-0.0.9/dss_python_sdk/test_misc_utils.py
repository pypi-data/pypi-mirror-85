# -*- coding: utf-8 -*-
__author__ = 'vivian'

import unittest
from dss_python_sdk.misc_utils import get_misc_properties


class TestDBUtils(unittest.TestCase):
    def test_get_queue_properties(self):
        url = "https://test.example.com/dss/misc"
        plat_key = "xx"
        svc_code = "xx"
        profile = "xx"
        user_agent = svc_code
        miscs = get_misc_properties(url, plat_key, svc_code, profile, user_agent)
        for (k, v) in miscs.items():
            print("rd-n:%s, ip:%s, port:%d, password:%s" %
                  (k, v["ip"], v["port"], v["password"]))
