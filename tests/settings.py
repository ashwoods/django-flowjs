

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))


SITE_ID = 1

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

INSTALLED_APPS = [
    'appconf',
    'flowjs',
    'tests',
]


SECRET_KEY = 'top_secret'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}
