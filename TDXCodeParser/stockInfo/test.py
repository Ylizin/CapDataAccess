#%% 
from StockQ import *
s = Stock('sh.600000')
r = Record('sh.600000')

data = s.get_df()

p = data['open']
(p>'12').sum()
buy = p<'11.4'
data[buy]['date']
for date in data[buy]['time']:
    r.buy(1000,date)
