# -*- coding: utf-8 -*-
from loguru import logger
import time 
import functools
 
# 日志耗时装饰器
def logtime(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        res = func(*args, **kwargs)
        end = time.perf_counter()
        logger.info('【%s】 took %.2f s' % (func.__name__, (end - start)))
        return res
    return wrapper 

'''
该日志不保存
'''
def lump_logs(guid,text):
    data_begin = f"\n-------------------- {guid} Begin --------------------\n\n"
    data_end = f"\n-------------------- {guid} End --------------------\n\n"
    logger.debug(f"{data_begin} {text} {data_end}")