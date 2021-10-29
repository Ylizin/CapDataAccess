import redis
pool = redis.ConnectionPool.from_url('redis://:aliali@148.70.35.123',db=0)
import json
from pydantic import BaseModel
from fastapi import FastAPI,Query
from typing import Optional,List



app = FastAPI()
@app.get('/shibor/')
def get_shibor(shibor_type:str=Query(...,description='shibor_type, ON,W1,W2,M1,M3,M6,M9,Y1'),num:int=Query(10,description='num of returned datas')):
    with redis.StrictRedis(connection_pool=pool,decode_responses=True) as conn:
        red_name = 'shibor-'+shibor_type
        res = [json.loads(d) for d in conn.zrange(red_name,-num,-1)]
    return res