# -*- coding: utf-8 -*- 
import time
import datetime


def validate_date(text):
    '''验证日期格式

    :param text: 待检索文本

    >>> validate_date('2020-05-20')
    True
    >>> validate_date('2020-05-32')
    False
    '''
    try:
        if text != time.strftime('%Y-%m-%d', time.strptime(text, '%Y-%m-%d')):
            raise ValueError
        return True
    except ValueError:
        return False


def validate_datetime(text):
    '''验证日期+时间格式

    :param text: 待检索文本

    >>> validate_datetime('2020-05-20 13:14:15')
    True
    >>> validate_datetime('2020-05-32 13:14:15')
    False
    '''
    try:
        if text != datetime.datetime.strptime(text, '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S'):
            raise ValueError
        return True
    except ValueError:
        return False
