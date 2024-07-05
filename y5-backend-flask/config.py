import os

from sshtunnel import SSHTunnelForwarder

# SSH server configuration
# ssh_host = 'ysj_5.soulfar.com'
# ssh_port = 22
# ssh_user = 'zhuoqi'
# ssh_private_key = '/Users/codingchan/.ssh/id_rsa'
#
# # MySQL server configuration
# mysql_host = '127.0.0.1'  # Localhost, as the tunnel endpoint
# mysql_port = 3306
# mysql_user = 'admin'
# mysql_password = 'maxwit'
# mysql_database = 'ysj_5'
#
# # Establish SSH tunnel
# tunnel = SSHTunnelForwarder(
#     (ssh_host, ssh_port),
#     ssh_username=ssh_user,
#     ssh_pkey=ssh_private_key,
#     remote_bind_address=(mysql_host, mysql_port)
# )
# tunnel.start()
# # Configure SQLAlchemy to use the SSH tunnel for connections
# SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{mysql_user}:{mysql_password}@{tunnel.local_bind_host}:{tunnel.local_bind_port}/{mysql_database}"
# print(SQLALCHEMY_DATABASE_URI)

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://admin:maxwit@ysj_5.soulfar.com:3306/ysj_5?charset=utf8mb4'
# SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://admin:maxwit@tmp.soulfar.com:3306/ysj_5?charset=utf8mb4'     # aliyun
# SQLALCHEMY_ECHO = True
SQLALCHEMY_POOL_RECYCLE = 300
SQLALCHEMY_POOL_SIZE = 100
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

# deprecated
TIMELINE_PUB = 0
TIMELINE_PRI = 1
TIMELINE_ALL = 2

# schedule
# JOBS = [
#     {
#         'id': 'job_mail_night',
#         'func': 'scheduler:task',
#         'args': None,
#         'trigger': 'cron',
#         'day': '*',
#         'hour': '20',
#         'minute': '0',
#         'second': '0'
#     }
# ]
SCHEDULER_API_ENABLED = True
