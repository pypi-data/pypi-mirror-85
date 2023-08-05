# -*- coding: utf-8 -*-
__author__ = 'vivian'

import unittest
from dss_python_sdk.db_utils import get_db_properties


class TestDBUtils(unittest.TestCase):
    def test_get_db_properties(self):
        url = "https://test.example.com/dss/db"
        plat_key = "xx"
        svc_code = "xx"
        profile = "xx"
        user_agent = svc_code
        databases = get_db_properties(url, plat_key, svc_code, profile, user_agent)
        for (k, v) in databases.items():
            print("dsn-n:%s, ip:%s, port:%d, sid:%s, username:%s, password:%s" %
                  (k, v["ip"], v["port"], v["sid"], v["username"], v["password"]))
