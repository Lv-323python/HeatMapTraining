from sanic import Sanic

app = Sanic()
app.static('/static', './app/static')

from app import routes
