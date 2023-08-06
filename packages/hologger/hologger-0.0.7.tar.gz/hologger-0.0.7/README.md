Before use this app you have to do few configuration.
In your setting.py add follow handlers and loggers.
If you want log your query, add 'dblogger_sql' to handlers and loggers. 

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class' : 'logging.StreamHandler'
        },
        'dblogger': {
            'level': 'DEBUG',
            'class': 'hologger.handlers.HoLogHandler',
        },
        'dblogger_sql':{
            'level' : 'DEBUG',
            'class' : 'hologger.handlers.HoLogSqlHandler'
        }
    },
    'loggers': {
        'dblogger': {
            'handlers': ['hologger'],
            'level': 'INFO',
            'propagate': True,
        },
        'django.db.backends':{
            'handlers': ['console', 'hologger_sql'],
            'level': 'DEBUG'
        }
    },
}


And add DATABASE ROUTER 'HoLoggingRouter'
DATABASE_ROUTERS = ['hologger.router.HoLoggingRouter']

Add 'hologger' to INSTALLED_APPS.
INSTALLED_APPS = [
    ...
    'hologger',
]


Add 'HoLoggingMiddleware' to MIDDLEWARE.
MIDDLEWARE = [
    ...
    'hologger.middleware.HoLoggingMiddleware',
]


Add 'ho_logger' to DATABASES.
DATABASES = {
    ...
    'ho_logger': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'logging',
        'USER': 'Your user name',
        'PASSWORD': 'Your password',
        'HOST': 'Your DB HOST.',
        'PORT': '3306',
        'ATOMIC_REQUESTS': True,
        'CONN_MAX_AGE': 60,
        'OPTIONS': {'charset': 'utf8mb4', 'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"}
    }
}