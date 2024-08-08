from pathlib import Path
from libs.env import env

APP_NAME = "Сервис рассылок"
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = "django-insecure-27r+^-=803(&$v1wl5%%zkeso7_bb!p$(=regy=u349n2j+^hc"
DEBUG = True
ALLOWED_HOSTS = []

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_apscheduler",

    "letters_sending",
    'authen',
    'blog'
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": env("DB_NAME"),
        "USER": env("DB_USER"),
        "PASSWORD": env("DB_PASSWORD"),
        "HOST": env("DB_HOST"),
        "PORT": env("DB_PORT"),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "ru-Ru"
TIME_ZONE = "Asia/Yakutsk"
USE_I18N = True
USE_TZ = False
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
DATETIME_FORMAT = "%Y-%m-%d %H:%M"
NULLABLE = {"null": True, "blank": True}

# СТАТИЧЕСКИЕ ФАЙЛЫ
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]

# МЕДИА ФАЙЛЫ
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# ПОЧТА
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = env("EMAIL_HOST")
EMAIL_PORT = env("EMAIL_PORT")
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True
EMAIL_HOST_USER = env("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")
SERVER_EMAIL = EMAIL_HOST_USER
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# АУТЕНТИФИКАЦИЯ И АВТОРИЗАЦИЯ
AUTH_USER_MODEL = "authen.User"
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# ПЛАНИРОВЩИК
APSCHEDULER_DATETIME_FORMAT = "N j, Y, f:s"
SCHEDULER_INTERVAL = 15
SCHEDULER_ACTIVE = False


