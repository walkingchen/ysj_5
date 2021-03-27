SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://admin:maxwit@ysj_5.soulfar.com:3306/ysj_5'
SQLALCHEMY_POOL_RECYCLE = 300
SQLALCHEMY_TRACK_MODIFICATIONS = False
# SQLALCHEMY_ECHO = True
CSRF_ENABLED = True

# flask-bootstrap
BOOTSTRAP_SERVE_LOCAL = True

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
