from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent


try:
    from django.urls import path
    HAS_PATH = True
except ImportError:
    HAS_PATH = False


try:
    from django.urls import re_path
    HAS_RE_PATH = True
except ImportError:
    HAS_RE_PATH = False


SECRET_KEY = 'test'


ROOT_URLCONF = 'tests.urls'


MIDDLEWARE = ['django.contrib.sessions.middleware.SessionMiddleware']


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'test.sqlite3',
    }
}


INSTALLED_APPS = [
    'tests',
]


STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'tests' / 'static'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'tests' / 'media'
