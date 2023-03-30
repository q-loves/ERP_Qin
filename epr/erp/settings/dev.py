"""
Django settings for erp project.

Generated by 'django-admin startproject' using Django 3.2.15.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import os
import sys
import datetime
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
from django.conf import global_settings

# BASE_DIR = Path(__file__).resolve().parent.parent
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#添加导包路径
sys.path.insert(0,os.path.join(BASE_DIR,'apps'))
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-fze(50fnd1qvzwvx3jy9-+izy0k49^d2&mng5n(mfca1p1q$dy'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'corsheaders',  # 跨域访问
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'erp_system',
    'drf_yasg',#配置接口文档
    'django_celery_results',#配置celery
    'basic_info',
    'good_info',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'erp.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'erp.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME':'erp',
        'USER':'erp',
        'PASSWORD':'erp',
        'HOST':'192.168.221.129',
        'PORT':3306,
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'zh-Hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

#redis数据库配置
CACHES = {
    "default": {  # 默认
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1/0",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    "session": {  # session
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    "verify_code": {  # 验证码
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1/2",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
}

#日志配置
# 配置项目日志
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,  # 是否禁用已经存在的日志器
    'formatters': {  # 日志信息显示的格式
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(filename)s: %(lineno)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(module)s %(lineno)d %(message)s'
        },
    },
    'filters': {  # 对日志进行过滤
        'require_debug_true': {  # django在debug模式下才输出日志
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {  # 日志处理方法
        'console': {  # 向终端中输出日志
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {  # 向文件中输出日志
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR,'logs/erp.log'),  # 日志文件的位置
            'maxBytes': 300 * 1024 * 1024,
            'backupCount': 10,
            'formatter': 'verbose'
        },
    },
     'loggers': {  # 日志器
        'erp': {  # 自己用的logger应用如下配置
          'handlers': ['console', 'file'],  # 上线之后可以把'console'移除
          'level': 'DEBUG',
          'propagate': True,  # 是否向上一级logger实例传递日志信息
        },
        'django': {  # 定义了一个名为django的日志器
            'handlers': ['console', 'file'],  # 可以同时向终端与文件中输出日志
            'propagate': True,  # 是否继续传递日志信息
            'level': 'INFO',  # 日志器接收的最低日志级别
        },
    }
}


#配置jwt
REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',

    'DEFAULT_AUTHENTICATION_CLASSES': (
        # DRF自带的JWT认证模块
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        ),
    # 'DEFAULT_PERMISSION_CLASSES': (
    #     'erp.utils.rbac_permission.RbacPermission',
    #
    #     ),
}
JWT_AUTH = {
    # 过期时间
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=1),

    'JWT_RESPONSE_PAYLOAD_HANDLER': 'erp.utils.jwt_response.jwt_response_payload_handler',
}
SWAGGER_SETTINGS={
    'REFETCH_SCHEMA_WITH_AUTH':True,
    'REFETCH_SCHEMA_ON_LOGOUT':True,
    'SECURITY_DEFINITIONS':{
        'JWT':{
            'type':'apiKey',
            'name':'Authorization',
            'in':'header'
        },
    }

}

#配置cors白名单
CORS_ORIGIN_WHITELIST=(
    'http://127.0.0.1:8080',
    'http://localhost:8080',
    'http://www.nagle.cn:8080',
    'http://api.nagle:8083',
)
CORS_ALLOW_CREDENTIALS = True # 允许携带cookie

#重新配置usermodel
AUTH_USER_MODEL = 'erp_system.UserModel'

#重写用户认证登陆类
AUTHENTICATION_BACKENDS = ['erp_system.auth.UserLoginAuth']

#celery配置
CELERY_TIMEZONE = "Asia/Shanghai"
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60
CELERY_CACHE_BACKEND = 'redis://127.0.0.1:6379/4'
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/5'
CELERY_RESULT_SERIALIZER='json'

BASE_API = 'api/'  # 项目BASE API, 如设置时必须以/结尾
# 权限认证白名单
WHITE_LIST = [f'/{BASE_API}user/login/', f'/{BASE_API}user/register/',  f'/swagger/.*']
REGEX_URL = '^{url}$'  # 权限匹配时,严格正则url

# MEDIA_ROOT= os.path.join(BASE_DIR,'media')
#
# MEDIA_URL = '/media/'

# 配置fastdfs图片路径
FDFS_BASE_URL = 'http://192.168.221.129:8888/'
DEFAULT_FILE_STORAGE = 'erp.utils.fastdfs.new_storage.NewFastdfsStorage'
FASTDFS_CONFIG_PATH=os.path.join(BASE_DIR,'utils/fastdfs/client.conf')