#%%
import talib
import numpy as np




CLOSE = None
OPEN = None
LOW = None
HIGH = None
VOLUME = None
AMOUNT = None
DATETIME = None

C = CLOSE
O = OPEN
L = LOW
H = HIGH
V = VOLUME
VOL = V
D = DATETIME




MA = talib.MA
WMA = talib.WMA
EMA = talib.EMA
STDDEV = talib.STDDEV
STD = STDDEV

SMA = lambda x,y,z: talib.SMA(x,y)
SUM = talib.SUM
ABS = np.abs

REF = lambda x,y: x[y]
MAX = np.maximum
MIN = np.minimum


def CROSS(s1,s2):
    cond1 = s1>s2
    cond2 = s1<= s2
    cond2 = cond2[:-1]
    cond1 = cond1[1:]
    return cond1 & cond2
CROSSOVER = CROSS

def COUNT(cond,n):
    result = np.full(len(cond), 0, dtype=np.int)
    series = cond
    for i in range(len(result)):
        result[-i-1] = np.sum(series[max(len(result)-i-n,0):len(result)-i])
    return result

def EVERY(cond,n):
    return COUNT(cond,n) == n

def HHV(s,n):
    result = np.full(len(s), 0, dtype=np.float64)
    series = s
    for i in range(len(result)):
        result[-i-1] = np.max(series[max(len(result)-i-n,0):len(result)-i])
    return result

def LLV(s,n):
    result = np.full(len(s), 0, dtype=np.float64)
    series = s
    for i in range(len(result)):
        result[-i-1] = np.min(series[max(len(result)-i-n,0):len(result)-i])
    return result

def IF(condition,true_statement,false_statement):
    condition = condition.astype(np.bool)
    result = np.full(len(condition), 0, dtype=np.float)
    if isinstance(true_statement,np.ndarray):
        result[condition] = true_statement[condition]
    else:
        result[condition] = true_statement
    if isinstance(false_statement,np.ndarray):
        result[~condition] = false_statement[~condition]
    else:
        result[~condition] = false_statement
    return result
IIF = IF

STICKLINE = lambda x,y,z,*_: IF(x,z,0)
DRAWTEXT = lambda x,y,z,*_: IF(x,1,0)