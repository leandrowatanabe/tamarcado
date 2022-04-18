from tamarcado.settings.base import *

DEBUG = True
ALLOWED_HOSTS = []
SECRET_KEY = 'django-insecure-%p7(tvf&1)!w9a_#9xx_vowyj!=$1iwk2(1t%uk4qwht$npwza'

LOGGING = {
    **LOGGING,
    'loggers':{
        '':{
            'level':'DEBUG',
            'handler':['console', 'file']
        }
    }
}