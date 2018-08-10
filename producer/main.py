"""
Module for creating a producer on Sanic which sends JSON to RabbitMQ
"""
import os
import json
from sanic import Sanic, response
from sanic.response import html
from sanic_wtf import SanicForm
from wtforms import SubmitField, TextField
import pika
from jinja2 import Template
import uuid
import time

app = Sanic()


# from app.request_sender_client_config import HOST, PORT, RPC_QUEUE


class RequestSenderClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.response = None
        self.corr_id = None

        print('Connecting to rabbitmg...')
        RETRIES = 30
        while True:
            try:
                # declare connection
                self.connection = pika.BlockingConnection(
                    pika.ConnectionParameters(host=self.host, port=self.port))
                self.channel = self.connection.channel()
                break
            except pika.exceptions.ConnectionClosed as exc:
                if RETRIES == 0:
                    print('Failed to connect!')
                    raise exc
                RETRIES -= 1
                time.sleep(1)
        print('Successfully connected!')

        # declare a queues
        queue = self.channel.queue_declare(queue='request')

        # declare a callback queue
        callback_queue = self.channel.queue_declare(
            queue='response')  # only allow access by the current connection
        self.callback_queue = callback_queue.method.queue  # queue name
        self.channel.basic_consume(self.on_response, no_ack=True, queue=self.callback_queue)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, message):
        self.corr_id = str(uuid.uuid4())

        self.channel.basic_publish(
            exchange='',
            routing_key='request',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=message
        )
        print('Waiting for response...')
        while self.response is None:
            self.connection.process_data_events()
        print('Response received!')
        return self.response


class FeedbackForm(SanicForm):
    """Provides basic form for input receiving from user"""
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
    """Routing function for main page"""
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
        return response.json(
            json.loads(RequestSenderClient('localhost', 8080).call(json.dumps(git_info))))
    return render_template('index.html')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
