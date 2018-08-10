from sanic import Sanic

app = Sanic()

from producer.app import routes
