# wiz_alilog


```python
from wiz_alilog.clent import AliLogClient
if __name__ == '__main__':
    with AliLogClient("cn-hongkong.log.aliyuncs.com", "project", "logstore", "keyid", "key") as c:
        res = c.query(query="query")
```