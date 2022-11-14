from __future__ import absolute_import, unicode_literals

import os

import dotenv
from pathlib import Path
import environ

env = os.environ.copy()


DEBUG = False


SECRET_KEY = os.getenv("SECRET_KEY")


ALLOWED_HOSTS = ["my_domain"]

BASE_DIR = Path(__file__).resolve().parent.parent
# use image db
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}



#  once frontend is up
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
]


# gmail while domain account is set up
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

