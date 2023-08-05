# -*- coding: utf-8 -*-
__author__ = 'vivian'

import yaml
from dss_python_sdk.http_utils import http_get
from dss_python_sdk.dss_utils import check_param
from dss_python_sdk.dss_utils import TIMEOUT


def get_db_properties(url, plat_key, svc_code, profile, user_agent):
    """
    Get database connection parameters
    :param url:
    :param plat_key:
    :param svc_code:
    :param profile:
    :param user_agent:
    :return:
    """
    check_param(url, plat_key, svc_code, profile, user_agent)
    prams = {"platkey": plat_key, "svccode": svc_code, "profile": profile}
    if user_agent.strip() == "":
        user_agent = svc_code
    res_bytes = http_get(url, user_agent, prams, TIMEOUT)
    d = yaml.load(res_bytes, Loader=yaml.FullLoader)
    try:
        ret_dict = d["database"]
        return ret_dict
    except TypeError:
        # It indicates that the server does not return db.yml file normally, either the PLATKEY is wrong,
        # or the SVCCODE is wrong, or the PROFILE is wrong.
        # If there is no problem in self-examination, contact the data source management system administrator
        raise Exception(res_bytes)
