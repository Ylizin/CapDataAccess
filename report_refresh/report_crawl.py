#%%
from celery import Celery
import requests
import json


_broker = r'redis://:aliali@148.70.35.123/3'
_backend = r'redis://:aliali@148.70.35.123/3'
app = Celery('crawler',broker=_broker,backend=_backend)

def parse_json(s):
    pos1 = s.index('(')+1
    pos2 = s.rindex(')')
    return s[pos1:pos2]

def get_json(url):
    res = requests.get(url)
    if '126.net' in url or 'sohu.com' in url:
        return json.loads(parse_json(res.text))
    return json.loads(res.text)

import redis
conn = redis.StrictRedis('148.70.35.123',password='aliali',db=0,decode_responses=True)
# conn = redis.StrictRedis('148.70.35.123',password='aliali',db=0)

#%%
import datetime
@app.task(name ='get_report')
def get_url_rep(code):
    report_url= r'https://stock.zsxg.cn/api/v2/report/list?code=' +code#研报url
    red_name = 'report-'+code 
    j = get_json(report_url)
    j = j['datas']
    parse_time = lambda x:datetime.datetime.fromisoformat(x['publishTime'][:-5]).timestamp()
    repos = {json.dumps(d):parse_time(d) for d in j}
    conn.zadd(red_name,repos)

