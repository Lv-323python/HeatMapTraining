"""Sanic"""
from sanic import Sanic
from sanic.response import html

APP = Sanic()


@APP.route('/')
def handle_request(request):
    """Routing"""
    template = open('./templates/index.html').read()
    return html(template)


if __name__ == "__main__":
    APP.run(host="0.0.0.0", port=8000, debug=True)
