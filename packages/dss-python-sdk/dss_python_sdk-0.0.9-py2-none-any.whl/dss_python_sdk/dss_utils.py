# -*- coding: utf-8 -*-
__author__ = 'vivian'

TIMEOUT = 3
PROFILE_RC1 = "rc1"
PROFILE_RC2 = "rc2"
PROFILE_PROD = "prod"


def check_param(url, plat_key, svc_code, profile, user_agent):
    if url is None or url.strip() == "":
        raise Exception("URL can't be empty string")
    if not url.startswith("https"):
        raise Exception("Only https protocol is supported ")
    if plat_key is None or plat_key.strip() == "":
        raise Exception("plat_key can't be empty string")
    if svc_code is None or svc_code.strip() == "":
        raise Exception("svc_code can't be empty string")
    if profile is None or profile.strip() == "":
        raise Exception("profile can't be empty string")
    if profile != PROFILE_RC1 and profile != PROFILE_RC2 and profile != PROFILE_PROD:
        raise Exception("profile error")
