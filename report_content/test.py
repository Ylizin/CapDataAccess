
# %%
import requests
import re
reg = re.compile('^[^\s\x21-\x2f\x3a-\x40\x5b-\x60\x7B-\x7F0-9\—\-_a-zA-Z\u4e00-\u9fa5\u3002\uff1b\uff0c\uff1a\u201c\u201d\uff08\uff09\u3001\uff1f\u300a\u300b]+')

url = r'http://pdf.dfcfw.com/pdf/H3_AP202101261454365286_1.pdf'
url2 = r'http://pdf.dfcfw.com/pdf/H3_AP202101251454124831_1.pdf'
resource_headers = requests.head(url=url2).headers

content_type = resource_headers.get('Content-Type','')
if content_type == 'application/pdf':
    content_length = int(resource_headers.get('Content-Length',''))
# %%
headers = {'authorization':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36'}
headers['Rane'] = 'bytes=0-{}'.format(content_length)
resp = requests.get(url=url2,headers=headers)
#%%
from tempfile import mkstemp,TemporaryFile
tmp = TemporaryFile()
tmp.write(resp.content)
# %%

from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer
texts = []
for page_layout in extract_pages(tmp):
    for element in page_layout:
        if isinstance(element, LTTextContainer):
            s = element.get_text() 
            print(s)
            print('------------')
            if len(s.strip())>10 and reg.match(s):
                texts.append(s[1:].replace('\n',''))