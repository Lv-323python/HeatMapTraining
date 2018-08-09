import os

import pika
from jinja2 import Template
from sanic import Sanic, response
from sanic.response import html
from sanic_wtf import SanicForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from pprint import pprint
from ast import literal_eval
import json

app = Sanic()


def render_template(html_name, **args):
    with open(os.path.join(os.path.dirname(__file__), 'templates', html_name), 'r') as f:
        html_text = f.read()
    template = Template(html_text)
    return html(template.render(args))


def sender(body):
    """

    :param body:
    :return:
    """
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='172.17.0.2'))
    channel = connection.channel()

    channel.queue_declare(queue='request')
    channel.queue_declare(queue='response')

    channel.basic_publish(exchange='',
                          routing_key='request',
                          body=body)

    def callback(ch, method, properties, body):
        """

        :param ch:
        :param method:
        :param properties:
        :param body:
        :return:
        """
        print(" [x] Received %r\n" % (body,))
        global result
        result = literal_eval(body.decode())
        pprint(result)
        channel.stop_consuming()
        return result

    channel.basic_consume(callback,
                          queue='response',
                          no_ack=True)

    channel.start_consuming()
    connection.close()
    return result


class IndexPage(SanicForm):
    git_client = StringField('Git Client', validators=[DataRequired])
    version = StringField('Version')
    token = StringField('Token')
    repository = StringField('Repository', validators=[DataRequired])
    owner = StringField('Owner', validators=[DataRequired])
    hash = StringField('Hash')
    branch = StringField('Branch')
    action = StringField('Action', validators=[DataRequired])
    submit = SubmitField('Submit')


@app.route("/", methods=["GET", "POST"])
async def index(request):
    form = IndexPage(request)
    if request.method == 'POST':
        git_client = form.git_client.data
        version = form.version.data
        token = form.token.data
        repository = form.repository.data
        owner = form.owner.data
        hash = form.hash.data
        branch = form.branch.data
        action = form.action.data
        request_dict = {'git_client': git_client,
                        'version': version,
                        'token': token,
                        'repo': repository,
                        'owner': owner,
                        'hash': hash,
                        'branch': branch,
                        'action': action}

        return response.json(sender(json.dumps(request_dict)))
    return render_template('index.html')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
