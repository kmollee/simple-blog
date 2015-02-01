"""
Django settings for sample project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages
from django.conf import global_settings
import imp

# os environ detect
# if is on openshift, debug off
# database location path to openshift data folder
ON_OPENSHIFT = False
if 'OPENSHIFT_REPO_DIR' in os.environ:
    ON_OPENSHIFT = True

# MYSQL or SQLITE3
DATABASE_CHOICE = 'MYSQL'

# WATSON or HAYSTACK
SEARCH_ENGINE = 'WATSON'

# path setting

# setting's etc folder path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# project's folder path
PROJECT_DIR = os.path.dirname(BASE_DIR)
# database folder
DATABASES_DIR = os.path.join(PROJECT_DIR, '..', 'database')
# templates folder
TEMPLATES_DIR = os.path.join(PROJECT_DIR, 'templates')
# static folder
STATIC_DIR = os.path.join(PROJECT_DIR, 'static')
# static root folder
STATIC_ROOT_DIR = os.path.join(PROJECT_DIR, '..', 'static')
# media folder
MEDIA_DIR = os.path.join(PROJECT_DIR, 'media')

# SECURITY WARNING: don't run with debug turned on in production!
if ON_OPENSHIFT:
    DEBUG = False
else:
    DEBUG = True

TEMPLATE_DEBUG = DEBUG


# host setting
if DEBUG:
    ALLOWED_HOSTS = ['127.0.0.1', 'localhost']
else:
    ALLOWED_HOSTS = ['*']

# secret key setting
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = ')w7o&0ly+ea^1vqe)113mcgqxqlnl3=8bqg)yuzm(5lx(#6*fc'
default_keys = {
    'SECRET_KEY': ')w7o&0ly+ea^1vqe)113mcgqxqlnl3=8bqg)yuzm(5lx(#6*fc'}
use_keys = default_keys
if ON_OPENSHIFT:
    imp.find_module('openshiftlibs')
    import openshiftlibs
    use_keys = openshiftlibs.openshift_secure(default_keys)
    SECRET_KEY = use_keys['SECRET_KEY']
else:
    if DEBUG:
        SECRET_KEY = default_keys['SECRET_KEY']
    else:
        from .key import key
        SECRET_KEY = key

# ====end serect key settnig====

# Application definition

DJANGO_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
)

LOCAL_APPS = (
    'apps.blog',
    'apps.account',
    'apps.todo',
)

THIRD_APPS = (
    #'django_extensions',
    'pagedown',
    'crispy_forms',
    #'django_jinja',
    'compressor',
)



# another template engine, in case
if 'django_jinja' in THIRD_APPS:
    # jinja2 template engine setting
    TEMPLATE_LOADERS = (
        'django_jinja.loaders.FileSystemLoader',
        'django_jinja.loaders.AppLoader',
    )

    # Same behavior of default intercept method
    # by extension but using regex (not recommended)
    DEFAULT_JINJA2_TEMPLATE_INTERCEPT_RE = r'.*jinja$'

if SEARCH_ENGINE == 'HAYSTACK':
    THIRD_APPS += ('haystack',)
else:
    THIRD_APPS += ('watson',)
INSTALLED_APPS = DJANGO_APPS + THIRD_APPS + LOCAL_APPS


# dev debug app
# if DEBUG:
#     INSTALLED_APPS += ('debug_toolbar',)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

# if DEBUG:
#     MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)


ROOT_URLCONF = 'etc.urls'

WSGI_APPLICATION = 'etc.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

if DATABASE_CHOICE == 'MYSQL':
    try:
        import pymysql
        pymysql.install_as_MySQLdb()
    except ImportError:
        pass
    if ON_OPENSHIFT:
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.mysql',
                'NAME': os.environ['OPENSHIFT_APP_NAME'],
                'USER': os.environ['OPENSHIFT_MYSQL_DB_USERNAME'],
                'PASSWORD': os.environ['OPENSHIFT_MYSQL_DB_PASSWORD'],
                'HOST': os.environ['OPENSHIFT_MYSQL_DB_HOST'],
                'PORT': os.environ['OPENSHIFT_MYSQL_DB_PORT']
            }
        }
    else:
        from . import mysqlaccount
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.mysql',
                'NAME': mysqlaccount.mysql_table,
                'USER': mysqlaccount.mysql_username,
                'PASSWORD': mysqlaccount.mysql_password,
            }
        }
else:
    if ON_OPENSHIFT:
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': os.path.join(os.environ['OPENSHIFT_DATA_DIR'], 'database', 'db.sqlite3'),
            }
        }
    else:
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': os.path.join(DATABASES_DIR, 'db.sqlite3'),
            }
        }

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

# TIME_ZONE = 'UTC'
TIME_ZONE = 'Asia/Taipei'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = STATIC_ROOT_DIR
STATICFILES_DIRS = (
    STATIC_DIR,
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # other finders..
    'compressor.finders.CompressorFinder',
)


TEMPLATE_DIRS = (
    TEMPLATES_DIR,
)

MEDIA_URL = '/media/'

if ON_OPENSHIFT:
    MEDIA_ROOT = os.path.normpath(
        os.path.join(os.environ['OPENSHIFT_DATA_DIR'], 'media'))
else:
    MEDIA_ROOT = MEDIA_DIR

# if not ON_OPENSHIFT:
#    TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

# NOSE_ARGS = [
#     '--with-coverage',
#     '--cover-package=blog',
#     '--cover-inclusive',
# ]

# crispy form template theme
CRISPY_TEMPLATE_PACK = 'bootstrap3'


#==== haystack search setting ====

if SEARCH_ENGINE == 'HAYSTACK':
    if ON_OPENSHIFT:
        WHOOSH_INDEX = os.path.normpath(
            os.path.join(os.environ['OPENSHIFT_DATA_DIR'], 'whoosh'))
    else:
        WHOOSH_INDEX = os.path.normpath(os.path.join(BASE_DIR, 'whoosh'))

    HAYSTACK_CONNECTIONS = {
        'default': {
            # this need to add custom lib to support chinese search
            # use jieja lib
            #'ENGINE': 'haystack.backends.whoosh_cn_backend.WhooshEngine',
            'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
            'PATH': WHOOSH_INDEX,
        }
    }
    HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'
    SEARCH_RESULTS_PER_PAGE = 20

#==== end haystack setting =====

# ==== session setting ====
# session could be remeber?
SESSION_REMEMBER = True
# session age unit second
# 1 hr
SESSION_COOKIE_AGE = 3600 * 6
# ==== end session setting ====

# ==== login logout url setting ====
LOGIN_REDIRECT_URL = reverse_lazy('account:index')
LOGIN_URL = reverse_lazy('account:login')
LOGOUT_URL = reverse_lazy('account:logout')
# ==== end login logout url setting ====

# ==== email setting ====
# email setting, use to send mail
# use gmail smtp
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587

OPEN_FORGET_PASSWORD = False

if OPEN_FORGET_PASSWORD:
    # import secret gmail account and password
    from .gmailAccount import *
    # ==== end email setting ====

OPEN_REGISTER = False

# change message tag ERROR to danger
# https://coderwall.com/p/wekglq/bootstrap-and-django-messages-play-well-together
# ajust css to bootstrap danger message
MESSAGE_TAGS = {
    messages.ERROR: 'danger'
}

# add context_processors for account function
# open forget password?
TEMPLATE_CONTEXT_PROCESSORS = global_settings.TEMPLATE_CONTEXT_PROCESSORS + (
    'apps.account.context_processors.open_forget_password',
    'apps.account.context_processors.open_register',
)

# let template can get request GET
TEMPLATE_CONTEXT_PROCESSORS += ("django.core.context_processors.request",)

# logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },

    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
