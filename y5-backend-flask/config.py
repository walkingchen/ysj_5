import os

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://admin:maxwit@ysj_5.soulfar.com:3306/ysj_5'
SQLALCHEMY_POOL_RECYCLE = 300
SQLALCHEMY_TRACK_MODIFICATIONS = False
# SQLALCHEMY_ECHO = True
CSRF_ENABLED = True

# flask-bootstrap
BOOTSTRAP_SERVE_LOCAL = True

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(PROJECT_ROOT)

# session
SECRET_KEY = 'dev'
SESSION_TYPE = 'redis'
# SESSION_KEY_PREFIX = 'flask'

# cache
CACHE_TYPE = 'redis'

# flask-admin config
# BABEL_DEFAULT_LOCALE = 'zh_CN'

# encoding
JSON_AS_ASCII = False

# title
ADMIN_TITLE = 'Admin'

# room init
MSG_SIZE_INIT = 50

DEBUG = True

UPLOAD_PATH = os.path.join(PROJECT_ROOT, 'uploads')
PHOTO_SIZE = {
    'small': 400,
    'medium': 800
}
PHOTO_SUFFIX = {
    PHOTO_SIZE['small']: '_s',  # thumbnail
    PHOTO_SIZE['medium']: '_m',  # display
}
