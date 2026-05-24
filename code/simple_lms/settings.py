SECRET_KEY = 'django-insecure-simple-lms-redis-key'
DEBUG = True
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.auth',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'lms_db',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'database',
        'PORT': '5432',
    }
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",

        "LOCATION": "redis://redis:6379/1",

        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },

        "TIMEOUT": 300,
    }
}