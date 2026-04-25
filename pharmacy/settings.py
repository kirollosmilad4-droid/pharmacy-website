import os
from pathlib import Path

# 📁 Base
BASE_DIR = Path(__file__).resolve().parent.parent

# 🔐 Security
SECRET_KEY = 'django-insecure-change-this-key'  # 🔥 غيره بعدين

DEBUG = False  # ❗ مهم في الإنتاج

ALLOWED_HOSTS = ['*']  # غيرها بعد ما تاخد لينك الموقع

# 📦 Apps
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'medicines',
]

# 🧠 Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # 🔥 مهم للـ static
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# 🌐 URLs
ROOT_URLCONF = 'pharmacy.urls'

# 🧾 Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['medicines/templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# ⚙️ WSGI
WSGI_APPLICATION = 'pharmacy.wsgi.application'

# 🗄️ Database (SQLite مؤقتًا)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# 🌍 Language
LANGUAGE_CODE = 'ar'
TIME_ZONE = 'Africa/Cairo'

USE_I18N = True
USE_TZ = True

# 📁 Static Files
STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / "static",
    BASE_DIR / "medicines/static",
]

STATIC_ROOT = BASE_DIR / 'staticfiles'

# 🔥 مهم مع Whitenoise
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# 📸 Media Files (الصور)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# 🔢 Default ID
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'