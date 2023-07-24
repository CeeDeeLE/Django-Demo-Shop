"""
Django settings for techmax project.

Generated by 'django-admin startproject' using Django 4.2.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-c#=dw*@sc%qj9uiw)q5r(pz_b974&if^vd!go8!zek7onmzjx!'

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True
DEBUG = False

# ALLOWED_HOSTS have to be provided in production mode!
# ALLOWED_HOSTS = []
ALLOWED_HOSTS = ["localhost", "127.0.0.1", ".vercel.app"]
# ALLOWED_HOSTS = ["localhost", "127.0.0.1", ".vercel.app", "*"]


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # ab hier Ergänzungen eingefügt
    'shop.apps.ShopConfig',
    'debug_toolbar',
    'paypal.standard.ipn',
]


# unbedingt auf 'False' setzen im Live-Betrieb mit echten Kunden-Daten !!!
PAYPAL_TEST = True


MIDDLEWARE = [
    # Debug-Toolbar-Ergänzung muss an erster Stelle erfolgen 
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    # bereits in Django integriert - für Cookie und User-Daten-Speicherung
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # CSRF-Token bereits integriert in Django
    'django.middleware.csrf.CsrfViewMiddleware',
    # bereits in Django integriert - für  User-Authentication
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    # bereits in Django integriert - für Popup-Messages
    'django.contrib.messages.middleware.MessageMiddleware',
    # Ergänzung für Click-Verfolgung
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'techmax.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            # wenn actions für alle Seiten zur Verfügung stehen sollen, ...
            # z.B. für die Badges über dem Warenkrob
            # context_processor ist der Name der neuen .py-Datei dafür
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'shop.context_processors.warenkorb_anzahl',
            ],
        },
    },
]

WSGI_APPLICATION = 'techmax.wsgi.app'
# WSGI_APPLICATION = 'techmax.wsgi.application'

# für flash messages -> hauptsächlich zum Styling
from django.contrib.messages import constants as messages

# Festlegung der Bootstrap-Klassen für das Erscheinungsbild der Messages
MESSAGE_TAGS = {
    messages.DEBUG: 'alert-secondary',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

INTERNAL_IPS = [  
    '127.0.0.1'  
]


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

STATICFILES_DIRS = [
    BASE_DIR / 'static',
]


# Ablageort für (hochgeladene) Bilddateien
MEDIA_URL = "/bilder/"

# 2 Wege, dasMedia-Verzeichnis einzubinden
# 1. import os
#    MEDIA_ROOT = os.path.join(BASE_DIR, 'static/bilder')
# 2. 
MEDIA_ROOT = BASE_DIR / "static/bilder"


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
