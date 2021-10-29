import json
from celery import Celery
from bs4 import BeautifulSoup, element
import requests
from collections import namedtuple
import json
import datetime
from enum import Enum,auto
#%%
from requests.api import get, request 
_broker = r'redis://:aliali@148.70.35.123/3'
_backend = r'redis://:aliali@148.70.35.123/3'
app = Celery('crawler',broker=_broker,backend=_backend)
import redis
conn = redis.StrictRedis('148.70.35.123',password='aliali',db=0,decode_responses=True)

_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.66'
}
base_url = r'http://data.eastmoney.com/shibor/'
# candidate_site = r'http://www.chinamoney.com.cn/chinese/bkshibor/' # 备选链接

class ShiborMap(Enum):
    ON= 0 
    W1 = 1
    W2 = auto()
    M1 = auto()
    M3 = auto()
    M6 = auto()
    M9 = auto()
    Y1 = auto()

shibor_map = {
    'ON':ShiborMap.ON, #隔夜
    'W1' :ShiborMap.W1, #1周
    'W2' :ShiborMap.W2,
    'M1' :ShiborMap.M1, #1月
    'M3' :ShiborMap.M3,
    'M6' :ShiborMap.M6,
    'M9' :ShiborMap.M9,
    'Y1' :ShiborMap.Y1
}

@app.task(name = 'get_shibor')
def get_shibor(shibor_type,page=1):
    if page<1 or page >10:
        page = 1
    con = requests.get(base_url+r'default.html',headers = _headers)
    con.encoding = 'gbk'
    doc = BeautifulSoup(con.text)
    trs = doc.find(id="tb").find_all('tr')[1:]
    url = base_url+trs[shibor_map[shibor_type].value].find("a")['href'].split('/')[-1]+'&p={}'.format(page)
    con = requests.get(url,headers = _headers)
    doc = BeautifulSoup(con.text)
    trs = doc.find(id="tb").find_all('tr')

    tds = [extract_tuple(item) for item in trs[1:]]
    parse_time = lambda dt:datetime.datetime.fromisoformat(dt['date']).timestamp()
    red_name = 'shibor-'+shibor_type
    return conn.zadd(red_name,{json.dumps(td):parse_time(td) for td in tds})

def extract_tuple(tds):
    res = {}
    elements = tds.text.split()
    res['date'] = elements[0]
    res['price'] = elements[1]
    res['change'] = elements[2]
    return res