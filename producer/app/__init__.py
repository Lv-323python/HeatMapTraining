from sanic import Sanic
from config import Config
from sanic_auth import Auth
from sanic_session import Session

app = Sanic(__name__)
app.static('/static', './app/static')
app.config.from_object(Config)
Session(app)
auth = Auth(app)

from app import routes
