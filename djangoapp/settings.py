import os

ROOT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEBUG = os.environ.get("DJANGO_DEBUG", False) in ("True", "true", "1")
SECRET_KEY = 1

USE_TZ = True

INSTALLED_APPS = [
    "django.contrib.staticfiles",
    "django.contrib.auth",
    "django.contrib.contenttypes",
]

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

STATIC_URL = "/static/"

DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": "db.sqlite3"}}

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
    }
]

MIDDLEWARE = [
    "abyss.django.AbyssMiddleware",
]

ROOT_URLCONF = "djangoapp.urls"
