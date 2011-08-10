# Django settings for gamedevid project.
import os
import sys

PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))

sys.path.append(os.path.join(PROJECT_PATH, 'apps'))
sys.path.append(os.path.join(PROJECT_PATH, 'libraries'))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
            ('kecebongsoft', 'kecebongsoft@gmail.com'),
         )

MANAGERS = ADMINS

#This is only being used locally
#We have settings_local.py (ignored in repo, create yourself), consists of only DATABASES var
#Override this in settings_local.py to use other database engine.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'gamedevid',
        'USER': 'root',
        'PASSWORD': '123',
        'HOST': 'localhost',
        'PORT': '',
    }
}

TIME_ZONE = 'America/Chicago'

LANGUAGE_CODE = 'en-us'

SITE_ID = 1

USE_I18N = True

USE_L10N = True

MEDIA_ROOT = PROJECT_PATH + '/media/'

MEDIA_URL = '/media/'

STATIC_ROOT = PROJECT_PATH + '/static/'

STATIC_URL = '/static/'

ADMIN_MEDIA_PREFIX = '/static/admin/'

STATICFILES_DIRS = (
        PROJECT_PATH + '/static-dev',
)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'legacies.users.backends.Authentication',
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

SECRET_KEY = '27_m6x(16_zz!=uc5)jr^u1%riua7k@-qk#bo%i=z(^7q$%6)l'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'sentry.client.middleware.Sentry404CatchMiddleware',
)
 
ROOT_URLCONF = 'gamedevid.urls'

TEMPLATE_DIRS = (
    PROJECT_PATH + '/templates/default',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
    'cores.context_processors.global_settings',
    'posts.context_processors.fetch_latest_posts',
    'images.context_processors.fetch_random_image',
    'tags.context_processors.list_sticky_tags',
)


INSTALLED_APPS = (
    # Core Site
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'south',
    'compressor',
    'sentry',
    'sentry.client',
    'mptt',
    'tinymce',
    'easy_thumbnails',

    # Site Apps
    'cores',
    'users',
    'home',
    'posts',
    'announcements',
    'tags',
    'images',
    'games',
    'avatars',
    'legacies.users',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
LOGIN_URL = '/users/login/'


# TinyMCE
TINYMCE_DEFAULT_CONFIG = {
    'mode' : "textareas",
    'theme' : "advanced",
    'plugins' : "autolink,lists,spellchecker,pagebreak,style,layer,table,save,advhr,advimage,advlink,emotions,iespell,inlinepopups,insertdatetime,preview,media,searchreplace,print,contextmenu,paste,directionality,fullscreen,noneditable,nonbreaking,xhtmlxtras,template,media",

    #// Theme options
    'theme_advanced_buttons1' : "bold,italic,underline,strikethrough,fontsizeselect,|,justifyleft,justifycenter,justifyright,justifyfull,|fontsizeselect,|,bullist,numlist,|,outdent,indent,blockquote,|,undo,redo,|,link,unlink,image,media,|,`insertdate,inserttime,preview,|,forecolor,backcolor",
    'theme_advanced_buttons2' : "",
    'theme_advanced_buttons3' : "",
    'theme_advanced_toolbar_location' : "top",
    'theme_advanced_toolbar_align' : "left",
    'theme_advanced_resizing' : 'true',

    #// Skin options
    'skin' : "o2k7",
    'skin_variant' : "black",  
    'content_css' : "/static/css/default/tinymce.css",
}

TAG_IMAGE_ID = 16
TAG_GAME_ID = 17

POST_CONTENT_UNALLOWED_TAGS = "pre"

try:
    from settings_local import *
except ImportError:
    pass
