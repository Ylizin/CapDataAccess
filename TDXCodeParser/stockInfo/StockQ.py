#%%
from datetime import date
import baostock as bs
import pandas as pd
import datetime


__login_info = bs.login()
class Stock:
    def __init__(self,stock_id,frequency = 'd',start_date = None,end_date = None,adjustflag = '2'):
        super().__init__()
        if not end_date:
            if start_date: # if has start date and no end date
                if frequency == 'd':
                    dt = datetime.datetime.strptime(start_date,r'%Y-%m-%d')
                end_date = (dt+datetime.timedelta(days=20)).strftime(r'%Y-%m-%d')
            dt = datetime.datetime.now()
            end_date = dt.strftime(r'%Y-%m-%d')
            start_date = (dt - datetime.timedelta(days=20)).strftime(r'%Y-%m-%d')



        # sh. / sz.
        self.stock_id = stock_id
        self.start_date = start_date
        self.end_date = end_date
        self.adjustflag = adjustflag
        # 默认为d，日k线；d=日k线、w=周、m=月、5=5分钟、15=15分钟、30=30分钟、60=60分钟k线数据
        self.frequency = frequency
        # a list of fields
        if self.frequency == 'd':
            self.fields = "date,code,open,close,high,low,volume,amount,adjustflag".split(',')
        else:
            self.fields = "date,time,code,close,open,high,low,volume,amount,adjustflag".split(',')
    
    def get_df(self):
        rs = bs.query_history_k_data_plus(self.stock_id,','.join(self.fields),start_date = self.start_date,end_date=self.end_date,frequency=self.frequency,adjustflag=self.adjustflag)
        if not rs.error_code == '0':
            print(rs.error_msg)
            return None
        self.data = rs.get_data()
        return self.data


from enum import Enum
class Operation(Enum):
    Buy = 1   
    Sell = 2


#%%
# demo to user time comparision in pandas 
# the time string can be compared directly
#
# to parse time:
# pd.to_datetime(d['time'],format=r'%Y%m%d%H%M%S%f')
#
# to get a time:
# for ti in t:
    # if ti > pd.Timestamp('2020-08-28 10:00:00'):
        # print(ti)
        # break
# so ti is the index of this time 
# and acess the data like df[ti], be careful that the index should be set to the timestamp
# like t.index = t or df.set_index(xx)
# d.loc[ti]
# 
# t>'2020-08-28 10:00:00'
# 0    False
# 1    False
# 2    False
# 3    False
# 4     True
# 5     True
# 6     True
# 7     True
# Name: time, dtype: bool

def find_first_slice(dates,date):
    for d in dates:
        if d >= date:
            return d

class Record:
    """
     A series of operations on a stock
    """
    def __init__(self,stock_id,fee_rate = 2/10000):
        super().__init__()
        self._stock_id = stock_id
        # list of (date,amount,operation)
        self._ops = []
        # cash remains
        self._cash = 0
        # holding stock amount
        self._hold = 0
        self.fee_rate = fee_rate
        self.base_fee = 5

    def buy(self,amount,date):
        self._ops.append((date,amount,Operation.Buy))

    def sell(self,amount,date):
        self._ops.append((date,amount,Operation.Sell))

    def get_cash(self):
        return self._cash

    def get_hold(self):
        return self._hold

    def calculate_profit(self,data):
        if 'time' in data:
            time_series = data['time']
            data = data.set_index('time')
        else:
            time_series = data['date']
            data = data.set_index('date')
        cash =  0
        hold = 0
        base_fee = 0
        fee = 0
        for date,amount,op in self._ops:
            if date<time_series.min() or date>time_series.max():
                continue
            s = find_first_slice(time_series,date)#pd.Timestamp(date))
            s = data.loc[s]
            pri = (float(s['open']) + float(s['close']))/2
            if op == Operation.Buy:
                hold += amount
                base_fee += self.base_fee
                fee = pri*amount*self.fee_rate
                cash -= pri*amount*(1+self.fee_rate) + self.base_fee
            else:
                base_fee += self.base_fee
                fee += pri*amount*self.fee_rate
                hold -= amount
                cash += pri*amount*(1-self.fee_rate) - self.base_fee
        return cash,hold,base_fee,fee
