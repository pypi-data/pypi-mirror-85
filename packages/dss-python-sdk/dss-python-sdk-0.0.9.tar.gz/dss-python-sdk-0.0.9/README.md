dss-python-sdk is a sdk for data source management system. 

1.Install 

`pip install dss-python-sdk`


2.Use

2.1 database
```python
from dss_python_sdk.db_utils import get_db_properties
url = "https://test.example.com/dss/db"
plat_key = "xx"
svc_code = "xx"
profile = "xx"
user_agent = svc_code
databases = get_db_properties(url, plat_key, svc_code, profile, user_agent)
for (k, v) in databases.items():
    print("dsn-n:%s, ip:%s, port:%d, sid:%s, username:%s, password:%s" %
          (k, v["ip"], v["port"], v["sid"], v["username"], v["password"]))
```

2.2 queue
```python
from dss_python_sdk.queue_utils import get_queue_properties
url = "https://test.example.com/dss/queue"
plat_key = "xx"
svc_code = "xx"
profile = "xx"
user_agent = svc_code
queues = get_queue_properties(url, plat_key, svc_code, profile, user_agent)
for (k, v) in queues.items():
    print("mq-n:%s, ip:%s, port:%d, vhost:%s, username:%s, password:%s" %
          (k, v["ip"], v["port"], v["vhost"], v["username"], v["password"]))
```

2.3 misc
```python
from dss_python_sdk.misc_utils import get_misc_properties
url = "https://test.example.com/dss/misc"
plat_key = "xx"
svc_code = "xx"
profile = "xx"
user_agent = svc_code
miscs = get_misc_properties(url, plat_key, svc_code, profile, user_agent)
for (k, v) in miscs.items():
    print("rd-n:%s, ip:%s, port:%d, password:%s" %
          (k, v["ip"], v["port"], v["password"]))
```