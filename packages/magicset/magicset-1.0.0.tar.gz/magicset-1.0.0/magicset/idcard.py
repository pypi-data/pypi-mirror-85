
# _*_ coding=utf-8 _*_
__author__  = "8034.com"
__date__    = "2018-04-16"


import random 
import time 
  
def idcard_generator(e_num=0,birthday_year=0, birthday_mon=0, birthday_date=0):  
    """ 随机生成新的18为身份证号码 idcard   """  
    ARR = (7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2)  
    LAST = ('1', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2')  
    t = time.localtime()[0]  
    erea_num = e_num if e_num else 110105
    birthday_year = birthday_year if birthday_year else random.randint(t - 80, t - 18)
    birthday_mon = birthday_mon if birthday_mon else random.randint(1, 12)
    birthday_date = birthday_date if birthday_date else random.randint(1, 28)
    x = '%6Ld%04d%02d%02d%03d' % (erea_num, birthday_year, birthday_mon, birthday_date, random.randint(1, 999)) 
    y = 0  
    for i in range(17):  
        y += int(x[i]) * ARR[i]  
    IDCard = '%s%s' % (x, LAST[y % 11])  
    # birthday = '%s-%s-%s 00:00:00' % (IDCard[6:14][0:4], IDCard[6:14][4: 6], IDCard[6:14][6:8])  
    return IDCard  

if __name__=='__main__':
    print(idcard_generator(e_num=110105,birthday_year=1990, birthday_mon=2,birthday_date=20))
    # 110105199003077817 北京市朝阳区
    p="LFNFVUOQA40010033"
    print(p[-5:])
    import datetime
    from time import strftime
    valid_datetime_start = datetime.date.today()    # 有效开始时间 
    valid_datetime_end = valid_datetime_start + datetime.timedelta(days=365*10)    # 有效截至时间

    pass 