import os
from datetime import timedelta
from pathlib import Path

DEBUG = os.environ.get("DEBUG", "True") != "FALSE"
if DEBUG:
    ALLOWED_HOSTS = ["*"]
    SECRET_KEY = "django-insecure-i-(^@udvkc6^^9mkwpn&8kk0!u0n-bn4$b4mfbii1(bzw_pq@"
    LOGLEVEL = "DEBUG"
    CORS_ALLOW_ALL_ORIGINS = True
else:
    ALLOWED_HOSTS = [os.environ["DOMAIN_URL"], "amuman-manager-staging" "localhost" "*"]
    SECRET_KEY = os.environ["SECRET_KEY"]
    LOGLEVEL = "INFO"
    SESSION_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SECURE_HSTS_SECONDS = 3600
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    CORS_ALLOW_ALL_ORIGINS = False

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "django_rich_logging": {
            "class": "django_rich_logging.logging.DjangoRequestHandler",
            "columns": [
                {"header": "Masdethod", "forawdmat": "[white]{method}", "style": "{"},
                {"header": "Path", "format": "[white bold]{path}", "style": "{"},
                {"header": "Size", "format": "[white]{size}", "style": "{"},
                {"header": "Status", "format": "{status_code}", "style": "{"},
                {
                    "header": "Time",
                    "format": "[white]{created}",
                    "style": "{",
                    "datefmt": "%H:%M:%S",
                },
            ],
        },
    },
    "loggers": {
        "django.server": {"level": "DEBUG", "handlers": ["django_rich_logging"]},
        "django.request": {"level": "CRITICAL"},
        "rich": {
            "handlers": ["django_rich_logging"],
            "level": "DEBUG",
            "propagate": True,
        },
    },
}
BASE_DIR = Path(__file__).resolve().parent.parent

INSTALLED_APPS = [
    "manager",
    "daphne",
    "corsheaders",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework_simplejwt.token_blacklist",
    "django_filters",
    "drf_spectacular",
    "channels",
    "constance",
]

CONSTANCE_CONFIG = {
    "autorun_jobs": (True, ""),
}


# Needed for the admin panel
STATIC_URL = "/static/"
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "manager/static"),
]
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")


CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("localhost", 6379)],
        },
    },
}

ASGI_APPLICATION = "amuman.asgi.application"


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "manager.middleware.scheduler_middleware.SchedulerMiddleware",
]
if DEBUG:
    MIDDLEWARE.append(
        "manager.middleware.generate_initial_data.GenerateRandomJobsMiddleware"
    )


ROOT_URLCONF = "amuman.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(BASE_DIR, "manager", "templates"),
        ],
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

WSGI_APPLICATION = "amuman.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": Path("/manager/db.sqlite3"),
    }
}
if DEBUG:
    DATABASES["default"] = {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "amuman_manager.sqlite3",
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


LANGUAGE_CODE = "en-us"

TIME_ZONE = "Europe/Warsaw"

USE_I18N = True

USE_TZ = True

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.BasicAuthentication",
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 10,
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(seconds=3600),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=360),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": True,
}

RUN_WEBSOCKET_CLIENT = True


CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}

URL_MODE_PREFIX = "manager"

APPEND_SLASH = True
