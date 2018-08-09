from sanic import Sanic, response
from sanic_wtf import SanicForm
from wtforms import SubmitField, TextField
from sanic.response import html, json
from producer.rmq_sender import send, receive
app = Sanic()
app.config['SECRET_KEY'] = 'top secret !!!'
session = {}


class FeedbackForm(SanicForm):
    git_client = TextField('git_client')
    token = TextField('token')
    repo = TextField('repo')
    owner = TextField('owner')
    hash = TextField('hash')
    branch = TextField('branch')
    action = TextField('action')
    submit = SubmitField('Submit')


@app.middleware('request')
async def add_session(request):
    request['session'] = session


@app.route('/', methods=['GET', 'POST'])
async def index(request):
    form = FeedbackForm(request)
    if request.method == 'POST' and form.validate():
        git_client = form.git_client.data
        token = form.token.data
        repo = form.repo.data
        owner = form.owner.data
        hash = form.hash.data
        branch = form.branch.data
        action = form.action.data
        result = response.json(
            {'git_client': git_client,
             'token': token,
             'repo': repo,
             'owner': owner,
             'hash': hash,
             'branch': branch,
             'action': action})
        return result
    receive()

    content = f"""
    <form action="" method="POST">
       {'<br>'.join(form.csrf_token.errors)}
      {form.csrf_token}
      <br>
      <span>Git Client</span>
      {form.git_client}<br>
      <span>Token</span>
      {form.token}<br>
      <span>Repository</span>
      {form.repo}<br>
      <span>Owner</span>
      {form.owner}<br>
      <span>Hash</span>
      {form.hash}<br>
      <span>Branch</span>
      {form.branch}<br>
      <span>Action</span>
      {form.action}<br>
      {form.submit}<br>
    </form>
    """
    return html(content)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
