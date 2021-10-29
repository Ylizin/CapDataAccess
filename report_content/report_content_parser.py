#%%
from celery import Celery
import requests
import re
from tempfile import mkstemp,TemporaryFile
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer

reg = re.compile('^[^\s\x21-\x2f\x3a-\x40\x5b-\x60\x7B-\x7F0-9\—\-_a-zA-Z\u4e00-\u9fa5\u3002\uff1b\uff0c\uff1a\u201c\u201d\uff08\uff09\u3001\uff1f\u300a\u300b]+')

_broker = r'redis://:aliali@148.70.35.123/3'
_backend = r'redis://:aliali@148.70.35.123/3'
app = Celery('crawler',broker=_broker,backend=_backend)
headers = {'authorization':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36'}


import redis
conn = redis.StrictRedis('148.70.35.123',password='aliali',db=0,decode_responses=True)
# conn = redis.StrictRedis('148.70.35.123',password='aliali',db=0)

#%%
import datetime
test_url = r'http://pdf.dfcfw.com/pdf/H3_AP202101261454365286_1.pdf'

@app.task(name ='get_report_content')
def get_rep_content(url):
    texts = []
    resource_headers = requests.head(url=url).headers
    content_type = resource_headers.get('Content-Type','')
    if content_type == 'application/pdf':
        content_length = int(resource_headers.get('Content-Length',''))
    else:
        return texts

    headers['Rane'] = 'bytes=0-{}'.format(content_length)
    resp = requests.get(url=url,headers=headers)
    tmp = TemporaryFile()
    tmp.write(resp.content)
    for page_layout in extract_pages(tmp):
        for element in page_layout:
            if isinstance(element, LTTextContainer):
                s = element.get_text() 
                if len(s.strip())>10 and reg.match(s):
                    texts.append(s[1:].replace('\n',''))
    return texts