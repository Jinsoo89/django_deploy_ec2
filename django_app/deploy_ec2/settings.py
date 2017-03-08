"""
Django settings for deploy_ec2 project.

Generated by 'django-admin startproject' using Django 1.10.6.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""
import json
import os

DEBUG = os.environ.get('MODE') == 'DEBUG'
print('DEBUG : {}'.format(DEBUG))

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT_DIR = os.path.dirname(BASE_DIR)
CONF_DIR = os.path.join(ROOT_DIR, '.conf-secret')
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')
STATIC_ROOT = os.path.join(BASE_DIR, 'static_root')

# static settings
STATIC_URL = '/static/'
STATIC_DIR = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [
    STATIC_DIR,
]
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# media settings

# settings_common.json을 불러와서 CONFIG_FILE_COMMON에 할당
CONFIG_FILE_COMMON = os.path.join(CONF_DIR, 'settings_common.json')
# settings_local.json의 경로를 CONFIG_FILE에 할당
CONFIG_FILE = os.path.join(CONF_DIR, 'settings_local.json' if DEBUG else 'settings_deploy.json')
# settings_deploy.json의 경로를 CONFIG_FILE_DEPLOY에 할당
CONFIG_FILE_DEPLOY = os.path.join(CONF_DIR, 'settings_deploy.json')
# CONFIG_FILE_COMMON경로의 파일을 읽어 json.loads()한 결과를 config_common에 할당
config_common = json.loads(open(CONFIG_FILE_COMMON).read())
# CONFIG_FILE경로의 파일을 읽어 json.loads()한 결과를 config에 할당
config = json.loads(open(CONFIG_FILE).read())
# CONFIG_FILE_DEPLOY경로의 파일을 읽어 json.loads()한 결과를 config_deploy에 할당
config_deploy = json.loads(open(CONFIG_FILE_DEPLOY).read())

# config_common의 내용을 현재 config에 합침
for key, key_dict in config_common.items():
    if not config.get(key):
        config[key] = {}
    for inner_key, inner_key_dict in key_dict.items():
        config[key][inner_key] = inner_key_dict
# print(config)
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config['django']['secret_key']

# SECURITY WARNING: don't run with debug turned on in production!


ALLOWED_HOSTS = config['django']['allowed_hosts']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'member',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'deploy_ec2.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            TEMPLATE_DIR,
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'deploy_ec2.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': config["db"]["engine"],
        'NAME': config["db"]["name"],
        'USER': config["db"]["user"],
        'PASSWORD': config["db"]["password"],
        'HOST': config["db"]["host"],
        'PORT': config["db"]["port"],
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators
AUTH_USER_MODEL = 'member.MyUser'
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
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'ko-kr'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/
