from sanic import Sanic
from config import Config

app = Sanic()
app.config.from_object(Config)

from app import routes
