# encoding: utf-8
'''
import datetime
import logging
import os
from loguru import logger

from ...settings.config import LOG_DIR 

try:
    log_level = os.environ['LOG_LEVEL']
except KeyError:
    log_level = 'INFO'  # pylint: disable=invalid-name (C0103)
 
today = datetime.datetime.now().strftime("%Y-%m-%d") 
log_file = os.path.join(LOG_DIR, "runtime-" + today + ".log") 

logger.add(log_file, encoding='utf-8', enqueue=True)
'''
    
     
