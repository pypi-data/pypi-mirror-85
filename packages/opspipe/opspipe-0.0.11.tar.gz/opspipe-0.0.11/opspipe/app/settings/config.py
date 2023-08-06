"""
系统配置
"""
import os
from ..models.db import outModels
# -----------------------系统调试------------------------------------
DEBUG = os.getenv('DEBUG', False)
INTERCEPT = True

# -----------------------项目信息------------------------------------
API_PREFIX = "/aip"
VERSION = "0.0.11"
PROJECT_NAME = "API_UNIFORM_INTERFACE"
DESCRIPTION = 'A simple uniform interface'
MDDOC_URL = '/mddoc'
OPENAPI_JSON = ''

# -----------------------数据库配置-----------------------------------
MYSQL_USER = os.getenv('MYSQL_USER', 'root')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', '123')
MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
MYSQL_PORT = os.getenv('MYSQL_PORT', 3306)
MYSQL_DB = os.getenv('MYSQL_DB', 'saas')

# -----------------------数据模型-------------------------------------
MODELS = outModels

# -----------------------数据库迁移-----------------------------------
TORTOISE_ORM = {
    "connections": {"default": f"mysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"},
    "apps": {
        "models": {
            "models": MODELS,
            "default_connection": "default",
        },
    },
}


# -----------------------redis--------------------------------------
REDIS_HOST = os.getenv('REDIS_HOST', '127.0.0.1')
REDIS_PORT = os.getenv('REDIS_PORT', 6379)
REDIS_DB = 0
REDIS_INIT = os.getenv('REDIS_INIT', '') # True、初始化 False、不初始化

# -----------------------跨域支持-------------------------------------
CORS_ORIGINS = ['http://localhost:5000']
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = ['*']
CORS_ALLOW_HEADERS = ['*']

# -----------------------模板、静态文件---------------------------------
ROOT_PATH = os.getcwd()
STATIC_DIR = os.path.join(ROOT_PATH, 'public')
TEMPLATE_DIR = os.path.join(STATIC_DIR, 'template')
MDDOC_DIR = os.path.join(STATIC_DIR, 'mddoc.md')
# -----------------------日志-----------------------------------------
LOG_DIR = os.path.join(ROOT_PATH, 'logs')

