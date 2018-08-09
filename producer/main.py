"""
Module for creating a producer on Sanic which sends JSON to RabbitMQ
"""
from sanic import Sanic, response
from sanic_wtf import SanicForm
from wtforms import SubmitField, TextField
from sanic.response import html
import pika
import os
from jinja2 import Template
import json

app = Sanic()


def sender(body):
    """
    Sends message to RabbitMQ and waiting for the response
    :param body:
    :return: message string
    """
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='172.17.0.4'))
    channel = connection.channel()

    channel.queue_declare(queue='request')
    channel.queue_declare(queue='response')

    channel.basic_publish(exchange='',
                          routing_key='request',
                          body=body)

    def callback(ch, method, properties, body):
        """
        Function which takes the message from response queue
        :param ch:
        :param method:
        :param properties:
        :param body:
        :return: message string
        """
        channel.stop_consuming()
        print(type(body.decode()))
        return body.decode()

    channel.basic_consume(callback,
                          queue='response',
                          no_ack=True)

    channel.start_consuming()
    connection.close()

    return body


class FeedbackForm(SanicForm):
    git_client = TextField('git_client')
    version = TextField('version')
    token = TextField('token')
    repo = TextField('repo')
    owner = TextField('owner')
    hash = TextField('hash')
    branch = TextField('branch')
    action = TextField('action')
    submit = SubmitField('Submit')


def render_template(html_name, **args):
    """
    Function which starts working with templates
    :param html_name:
    :param args:
    :return: html template
    """
    with open(os.path.join(os.path.dirname(__file__), 'templates', html_name), 'r') as f:
        html_text = f.read()
    template = Template(html_text)
    return html(template.render(args))


@app.route('/', methods=['GET', 'POST'])
async def index(request):
    form = FeedbackForm(request)
    if request.method == 'POST':
        git_client = form.git_client.data
        token = form.token.data
        version = form.version.data
        repo = form.repo.data
        owner = form.owner.data
        hash = form.hash.data
        branch = form.branch.data
        action = form.action.data
        git_info = {
            'git_client': git_client,
            'token': token,
            'version': version,
            'repo': repo,
            'owner': owner,
            'hash': hash,
            'branch': branch,
            'action': action}
        return response.json(json.loads(sender(json.dumps(git_info))))
    return render_template('index.html')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
