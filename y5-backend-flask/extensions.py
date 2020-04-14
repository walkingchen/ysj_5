from flask_cache import Cache
from flask_socketio import SocketIO
from flask_apscheduler import APScheduler
from flask_sqlalchemy import SQLAlchemy


cache = Cache(config={'CACHE_TYPE': 'simple'})
socketio = SocketIO()
db = SQLAlchemy()
scheduler = APScheduler()
