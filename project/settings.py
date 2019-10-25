"""
このファイルはDjangoの設定ファイルである. manage.pyより読み込まれる.
"""

import os

# 環境ごとに違う設定を用いる部分はlocal.pyに定義
from project.local import *


# アプリケーションの定義

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'code_essay.apps.CodeEssayConfig', # メインアプリを追加
    'sign.apps.SignConfig', # ユーザ管理用のアプリを追加
]

# ミドルウェアの定義

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# URLのルーティングの設定

ROOT_URLCONF = 'project.urls'

# テンプレートの設定

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

# wsgiの設定

WSGI_APPLICATION = 'project.wsgi.application'

# アカウント管理の際のパスワードのバリデータ設定

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

# ネットワーク環境の設定など

LANGUAGE_CODE = 'ja'
TIME_ZONE = 'Asia/Tokyo'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# 静的ファイルの設定

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# メディアファイルの設定

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# メディアファイルに関して (2019.10.21)
#
# メディアファイルの保存などの操作は現時点では実装していない.
# 実装の場合は TODO: Media としてコメントアウトしている部分をコメントアウト解除すると,
# メディアファイルなどの設定が利用できる.
# またこれらの実装には最新のPillowをpipでインストールすること.

# カスタマイズされたユーザーモデルを使用

AUTH_USER_MODEL = 'sign.User'

# ログイン画面

LOGIN_URL = 'sign:login'

# ログインした後のデフォルトのページ遷移

LOGIN_REDIRECT_URL = 'code_essay:article'

# メール送信設定

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_HOST_USER = ''
# EMAIL_HOST_PASSWORD = ''
# EMAIL_USE_TLS = True
# DEFAULT_FROM_EMAIL = ''
