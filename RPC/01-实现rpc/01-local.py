# -*- coding:utf8 -*-
# write by xiimao


class InvalidOperation(Exception):
    def __init__(self,message):
        self.message = message or 'Invalid operation'

def divide(num1, num2 = 1):
    '''
    除法
    :param num1: int
    :param num2: int
    :return: float
    '''
    if num2 == 0:
        raise InvalidOperation()
    return num1/num2

try:
    val = devide(200,100)

except InvalidOperation as e:
    print(e.message)

else:
    print(val)



#divide消息协议
# float divide(1:int num1, 2:int num2=1) => InvalidOperation


