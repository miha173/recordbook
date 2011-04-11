# -*- coding: UTF-8 -*-
# Don't modify this file!

import os

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Komkov Alexander', 'sashakomkov@gmail.com'),
)

MANAGERS = ADMINS

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__));

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'odaybook',            # Or path to database file if using sqlite3.
        'USER': 'root',                  # Not used with sqlite3.
        'PASSWORD': '123',               # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Moscow'

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

MEDIA_ROOT = os.path.join(PROJECT_DIR, "..", "media")

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'ru-ru'

SITE_ID = 1

#Количество объектов на странице с пагинатором
PAGINATOR_OBJECTS = 50

LOGIN_REDIRECT_URL = '/'

USE_I18N = True

USE_L10 = True

SOUTH_APPS = ['odaybook.attendance', 'odaybook.billing', 'odaybook.curatorship', 'odaybook.marks', 'odaybook.pages', 'odaybook.tests', 'odaybook.userextended']

MEDIA_URL = '/media/'

ADMIN_MEDIA_PREFIX = '/admin-media/'

SECRET_KEY = '_dyte-9u%m06vwhoyc7ug0n&4olty8*yx+sei8p_zet+)!v8wg'

TEMPLATE_LOADERS = (
    'odaybook.utils.load_template_from_app',
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

TEMPLATE_CONTEXT_PROCESSORS = (
                               "django.core.context_processors.auth",
                               "django.core.context_processors.media",
                               'odaybook.context_processors.plural',
                               'odaybook.context_processors.menu',
                               'odaybook.context_processors.environment',
                               'django.contrib.messages.context_processors.messages',
                               )


MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    #'django.contrib.auth.middleware.AuthenticationMiddleware',
    'odaybook.userextended.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'odaybook.urls'

TEMPLATE_DIRS = (
)

#Таймаут для входа/выхода (мин)
TIMEOUT = 20

#Дни недели
WORKDAYS = ( ('1', 'Понедельник'), 
             ('2', 'Вторник'), 
             ('3', 'Среда'), 
             ('4', 'Четверг'), 
             ('5', 'Пятница'), 
             ('6', 'Суббота')
)

#Номера уроков
LESSON_NUMBERS = ( ('1', '1'), 
                   ('2', '2'), 
                   ('3', '3'),
                   ('4', '4'),
                   ('5', '5'),
                   ('6', '6'),
                   ('7', '7'),
                   ('8', '8'),
                   ('9', '9'),
                   ('10', '10')
)


APPEND_SLASH = True

REST_MODELS = ['school', 'grade', 'teacher', 'pupil', 'subject', 'lesson', 'mark', 'resultdate', 'result']
REST_MODELS2APPS = {'school':      ['odaybook.userextended.models.School', 'forms.SchoolRestForm'],
                    'grade':       ['odaybook.userextended.models.Grade', 'forms.GradeRestForm'],
                    'teacher':     ['odaybook.userextended.models.Teacher', 'forms.TeacherRestForm'],
                    'pupil':       ['odaybook.userextended.models.Pupil', 'forms.PupilRestForm'],
                    'subject':     ['odaybook.userextended.models.Subject', 'forms.SubjectRestForm'],
                    'lesson':      ['odaybook.marks.models.Lesson', 'forms.LessonRestForm'],
                    'mark':        ['odaybook.marks.models.Mark', 'forms.MarkRestForm'],
                    'resultdate':  ['odaybook.marks.models.ResultDate', 'forms.ResultDateRestForm'],
                    'result':      ['odaybook.marks.models.Result', 'forms.ResultRestForm'],
                    }


BASIC_WWW_AUTHENTICATION = True

DATE_FORMAT = "d.m.y"

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.messages',
    
    'south',
    'pytils',
    'smart_selects',
    
    'odaybook',
    'odaybook.attendance',
    'odaybook.pages',
    'odaybook.userextended',
    'odaybook.marks',
    'odaybook.curatorship',
    'odaybook.tests',
    'odaybook.rest',
    'odaybook.api',
    'odaybook.billing',
)


# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
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
        'django.request':{
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}