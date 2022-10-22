from .base import *

DEBUG = False
ALLOWED_HOSTS = ["*"]

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'mssql',
        'NAME': config('MSSQL_NAME'),
        'USER': config('MSSQL_USERNAME'),
        'PASSWORD': config('MSSQL_PASSWORD'),
        'HOST': config('MSSQL_HOST'),
        'PORT': config('MSSQL_PORT'),
        'OPTIONS': {
            'driver': 'ODBC Driver 17 for SQL Server',
        },
    },
}

# Logging
LOGGING ={
    'version':1,
    'loggers':{
        'django':{
            'handlers':['file'],
            'level':'DEBUG'
        }
    },
    'handlers':{
        'file':{
            'level':'INFO',
            'class': 'logging.FileHandler',
            'filename':'./logs/info.log',
            'formatter':'simpleRe',
        }
    },
    'formatters':{
        'simpleRe': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        }
    }
}