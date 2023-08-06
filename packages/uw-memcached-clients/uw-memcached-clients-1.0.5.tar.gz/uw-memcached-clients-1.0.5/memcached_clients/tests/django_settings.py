SECRET_KEY = "xxxxxx"
INSTALLED_APPS = ["django_backend"]

DATABASES = {
    "default": {
        "NAME": ":memory:",
        "ENGINE": "django.db.backends.sqlite3",
    },
}

CACHES = {
    "default": {
        "BACKEND": "memcached_clients.django_backend.PymemcacheCache",
        "LOCATION": "127.0.0.1:11211",
        "OPTIONS": {
            "use_pooling": True,
            "max_pool_size": 4,
        },
    },
}

SESSION_ENGINE = "django.contrib.sessions.backends.cache"
