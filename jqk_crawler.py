import json
from celery import Celery
from bs4 import BeautifulSoup
import requests
from collections import namedtuple
import json
from requests.api import get, request 
_broker = r'redis://:aliali@148.70.35.123/3'
_backend = r'redis://:aliali@148.70.35.123/3'
app = Celery('crawler',broker=_broker,backend=_backend)


# %%
url = r'http://data.10jqka.com.cn/market/lhbyyb/orgcode/ZXZQGFYXGSBJZBZQYYB/'
_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.66'
}
con = requests.get(url,headers = _headers)
# %%
doc = BeautifulSoup(con.text)

name = doc.find(class_='left fl').find('h2').text
body = doc.find(class_='m-table m-table-nosort').find('tbody').find_all('tr')
items = [ele.find_all('td') for ele in body]

def extract_tuple(tds):
    res = {}
    res['date'] =tds[0].text
    tmp= tds[1].find('a')
    res['code'] = tmp['href'].split(r'/')[4]
    res['code_name'] = tmp.text
    res['reason'] = tds[2].text

    res['price'] = float(tds[3].text)
    res['buy'] = float(tds[4].text)
    res['sell'] = float(tds[5].text)
    res['bms'] = float(tds[6].text)
    return res
t = [extract_tuple(item) for item in items]
# stock_t = namedtuple('stock_t',['date','code','code_name','reason','price','buy','sell','bms'])