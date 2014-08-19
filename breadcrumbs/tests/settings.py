# coding=utf-8

DEBUG = True

SITE_ID = 1

SECRET_KEY = 'blabla'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
    }
}

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.contenttypes',
    'django.contrib.sites',
    'breadcrumbs.tests',
    'breadcrumbs',
]

ROOT_URLCONF = 'breadcrumbs.tests.urls'