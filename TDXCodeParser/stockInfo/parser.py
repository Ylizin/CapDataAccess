#%%
# rules:
# : -> export vars
# := -> define and value a var
# a function is the content before the first comma 
# color or stick definitions means exported vars
# if conditions
# stick line(cond,0,to return price,0,0)
# & add a pair of bracket to the next finished statement
# a statement is a 
 
# """
# N:=5;
# VAR1:4*SMA((CLOSE-LLV(LOW,N))/(HHV(HIGH,N)-LLV(LOW,N))*100,5,1)-
# 3*SMA(SMA((CLOSE-LLV(LOW,N))/(HHV(HIGH,N)-LLV(LOW,N))*100,5,1),3.2,1),COLORYELLOW,LINETHICK0;
# VAR2:8,COLORGREEN,LINETHICK0;
# 上升在即: IF(CROSS(VAR1,VAR2),80,0),STICK,COLOR0000CC,LINETHICK2;
# 专吸庄血: IF(VAR1<=8,25,0),STICK,COLORWHITE,LINETHICK2;
# DRAWTEXT(CROSS(VAR1,VAR2),80,'准备买入'),COLOR00FFFF;
# VARO5:=LLV(LOW,27);
# VARO6:=HHV(HIGH,34);
# VARO7:=EMA((CLOSE-VARO5)/(VARO6-VARO5)*4,4)*25;
# 建仓区: IF((VARO7<10),80,100) ,COLOR00CCFF,LINETHICK1;
# 0,LINETHICK2 ,COLORFFCC00;
# """

tdx_func = """
VARC:=LOW;
VARD:=REF(LOW,1);
VARE:=SMA(ABS(VARC-VARD),3,1)/SMA(MAX(VARC-VARD,0),3,1)*100;
VARF:=MA(VARE/10,3);
VAR10:=LLV(LOW,30);
VAR11:=HHV(VARF,30);
光头就买:MA(IF(LOW<=VAR10,(VARF+VAR11*2)/2,0),3);
VAR1B:=REF((LOW+OPEN+CLOSE+HIGH)/4,1);
VAR2B:=SMA(ABS(LOW-VAR1B),13,1)/SMA(MAX(LOW-VAR1B,0),10,1);
VAR3B:=EMA(VAR2B,10);
VAR4B:=LLV(LOW,33);
VAR5B:=EMA(IF(LOW<=VAR4B,VAR3B,0),3)*3;
主力进场:IF(VAR5B>REF(VAR5B,1),VAR5B,0),COLORRED,LINETHICK6;
STICKLINE(VAR5B>REF(VAR5B,1),0,VAR5B,3,0 ),COLORRED;
洗盘:IF(VAR5B<REF(VAR5B,1),VAR5B,0),COLORGREEN;
VAR1:=REF((LOW+OPEN+CLOSE+HIGH)/4,1);
VAR2:=SMA(ABS(LOW-VAR1),13,1)/SMA(MAX(LOW-VAR1,0),10,1);
VAR3:=EMA(VAR2,10);
VAR4:=LLV(LOW,33);
VAR5:=EMA(IF(LOW<=VAR4,VAR3,0),3);
STICKLINE(VAR5>REF(VAR5,1),0,VAR5,6,0 ),COLORGREEN;
STICKLINE(VAR5<REF(VAR5,1),0,VAR5,6,0),COLORRED;
找主力吸筹提款:(VAR5>REF(VAR5,4))AND C>REF(C,1),COLORFFFF00;
VAR2C:=(HIGH+LOW+CLOSE*2)/4;
VAR3C:=EMA(VAR2C,7);
VAR4C:=STD(VAR2C,7);
VAR5C:=(VAR2C-VAR3C)*100/VAR4;
VAR6C:=EMA(VAR5C,3);
WW:(EMA(VAR6C,5)+100)/2-3,COLORFF00FF;
MM:HHV(WW,3),COLORFF3333;
AAA:=AMOUNT/VOL/100;

"""
### str.rindex
###
###
import regex

# r_func = r'(\:|\:\=)?(\w*)\(.*\)(.*,|;)'
# func_re = regex.compile(r_func)

func_name = r'\w*\('
pre_var = r'^\w*\:(\=)?'
# 用正则先去匹配这两个部分，然后再用栈去做括号的匹配
var_re = regex.compile(pre_var)
func_name_re = regex.compile(func_name)

from .StockQ import Stock
# using from xxx import a =====> 
# import xxx.a
# a = xxx.a
# so xxx.a = b does not change the reference a in this file 
# only if a is an instance and set values by methods
from .TAFunc import *


def set_data(data):
    global CLOSE,OPEN,LOW,HIGH,VOLUME,AMOUNT,DATETIME,C,O,L,H,V,VOL,D
    CLOSE = data['close'].apply(float).to_numpy()
    OPEN = data['open'].apply(float).to_numpy()
    LOW = data['low'].apply(float).to_numpy()
    HIGH = data['high'].apply(float).to_numpy()
    VOLUME = data['volume'].apply(float).to_numpy()
    AMOUNT = data['amount'].apply(float).to_numpy()
    DATETIME = data['date']

    C = CLOSE
    O = OPEN
    L = LOW
    H = HIGH
    V = VOLUME
    VOL = V
    D = DATETIME

def find_next_stat(s):
    brackets = []
    for i,c in enumerate(s):
        if (c == ',' or c == ';') and len(brackets)==0: 
            break
        if c == '(':
            brackets.append(c)
        elif c == ')': # pop a ')', if not matched, is the end of a statement
            if not brackets:
                break
            if brackets.pop()=='(':
                pass
            else: 
                return None 
    stat = s[:i]
    return stat,i

def extract_fun(func_str):
    # read chars, if meet the first ( start count
    # push it into a stack
    # then if the stack is clean and we meet a comma, we just end 
    brackets = []
    res = ''
    matched = False 
    go_forward = 0
    for i,c in enumerate(func_str):
        a_o_pos = False
        if go_forward>0:
            go_forward -= 1
            continue
        if (c == ',' or c == ';') and matched and len(brackets)==0: 
            # if already matched 
            # and stack is empty 
            # and a new comma is encountered 
            return res

        if c == '&' or c=='|':
            a_o_pos = True
            stat,go_forward = find_next_stat(func_str[i+1:])

        if c == '(':
            brackets.append(c)
            matched = True 

        elif c == ')': # pop a ')', if not return err; 
            if brackets.pop()=='(':
                pass
            else: 
                return None 
        
        if not a_o_pos:
            res += c
        else:
            res += c+'('+stat+')'

# this function may need to be exec in multiprocessing
# cause multithreading can not switch vars like CLOSE,OPEN unpainfully         
def func_exec(func_s = tdx_func,data = None,code = 'sh.600000',**kwargs):
    """
    func at every time step we call this func to get some indicator

    Args:
        func_s (string): string of funcs
    """
    if not data:
        s = Stock(code,**kwargs)
        data = s.get_df()
    set_data(data)

    exports = {}
    lines = []
    cache = ''
    for line in func_s.split('\n'): # process one line each time 
        if not line:
            continue
        if not line.endswith(';'):
            cache += line
            continue
        line = cache+line
        cache = ''
        line = line.replace('AND','&')
        line = line.replace('OR','|')

        var = var_re.search(line)
        export = False 
        var_name = ''
        if var: # there is a prefix
            spans = var.span()
            prefix = var.group(0)
            if prefix.endswith(':'): #exports
                export = True 
                var_name = line[:spans[1]-1]
            else:
                export = False
                var_name = line[:spans[1]-2]
        
        line = var_re.sub('',line) # drop the var declaration
        func = func_name_re.search(line)

        expr = line
        if not func: # simple assign statement
            expr = expr.split(';')[0].split(',')[0]
        else: # need to sep a func statement 
            expr = extract_fun(expr)
            if '&' in expr:
                statements = expr.split('&')
                expr = '({}) & ({})'.format(statements[0],statements[1])
        if not export:
            if var_name:
                expr = var_name + ' = ' + expr 
                exec(expr)
            else: # no var, then its a line
                lines.append(eval(expr))
        else:
            exports[var_name] = eval(expr)
            if var_name:
                exec('{} = exports[\"{}\"]'.format(var_name,var_name))
    return exports,lines
