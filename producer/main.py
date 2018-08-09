"""Sanic"""
import jinja2
import jinja2_sanic
import pika
from pprint import pprint
from ast import literal_eval
from sanic import Sanic
from sanic_wtf import SanicForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

APP = Sanic()
template = "<html><body><h1>{{Player}}</h1>{{Category}}</body></html>"
jinja2_sanic.setup(
    APP,
    loader=jinja2.DictLoader(
        {
            "templates.jinja2": template
        }
    )
)


class IndexPage(SanicForm):
    git_client = StringField('Git Client', validators=[DataRequired])
    token = StringField('Token', validators=[DataRequired])
    repository = StringField('Repository', validators=[DataRequired])
    owner = StringField('Owner', validators=[DataRequired])
    hash = StringField('Hash', validators=[DataRequired])
    branch = StringField('Branch', validators=[DataRequired])
    action = StringField('Action', validators=[DataRequired])
    submit = SubmitField('Submit')


class Producer:
    def __init__(self, queue):
        """Set up the basic connection, and start a new thread for processing.
            1) Setup the pika connection, channel and queue.
            2) Start a new daemon thread.
        """
        self.queue = queue
        self.connection = pika.BlockingConnection()
        self.channel = self.connection.channel()
        result = self.channel.queue_declare(exclusive=True)
        self.callback_queue = result.method.queue


def sender(body):
    '''

    :param body:
    :return:
    '''

    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='172.17.0.2'))
    channel = connection.channel()

    channel.queue_declare(queue='request')
    channel.queue_declare(queue='response')

    channel.basic_publish(exchange='',
                          routing_key='request',
                          body=body)

    def callback(ch, method, properties, body):
        '''

        :param ch:
        :param method:
        :param properties:
        :param body:
        :return:
        '''

        print(" [x] Received %r\n" % (body,))
        result = literal_eval(body.decode())
        pprint(result)
        channel.stop_consuming()

    channel.basic_consume(callback,
                          queue='response',
                          no_ack=True)

    channel.start_consuming()
    connection.close()
    return body


@APP.route('/', methods=['GET', 'POST'])
@jinja2_sanic.template("templates.jinja2")
def index(request):
    """Routing"""
    form = IndexPage(request)
    if request.method == 'POST' and form.validate():
        git_client = form.git_client
        token = form.token
        repository = form.repository.data
        owner = form.owner.data
        hash = form.hash.data
        branch = form.branch.data
        action = form.action.data
        request_dict = {'git_client': git_client,
                        'token': token,
                        'repository': repository,
                        'owner': owner,
                        'hash': hash,
                        'branch': branch,
                        'action': action}
        return sender(request_dict)



if __name__ == "__main__":
    APP.run(host="0.0.0.0", port=8000, debug=True)
