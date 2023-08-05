# -*- coding: utf-8 -*-
__author__ = 'vivian'

import unittest
from dss_python_sdk.memory_utils import get_mem_properties


class TestDBUtils(unittest.TestCase):
    def test_get_queue_properties(self):
        url = "https://test.example.com/dss/mem"
        plat_key = "xxx"
        svc_code = "xxx"
        profile = "xxx"
        user_agent = svc_code
        miscs = get_mem_properties(url, plat_key, svc_code, profile, user_agent)
        for (k, v) in miscs.items():
            print("mem-n:%s, server_path:%s, mount_path:%s " %
                  (k, v["server_path"], v["mount_path"]))
