# -*- coding: utf-8 -*-

def life(args):
    '''
    this is my First Python Package.
    '''
    res = False
    if type(args) == int:
        sum = 0 
        for i in range(args + 1):
            sum += i
        res = True
    else:
        sum = '{0} 不是整数，无法计算'.format(args)
    return res, sum