import pathlib
import os
import requests
from google.oauth2 import id_token
from pip._vendor import cachecontrol
from flask import Flask, render_template, request, jsonify, make_response, session, abort, redirect, url_for
from google_auth_oauthlib.flow import Flow
import google.auth.transport.requests
import random
import time


app = Flask(__name__)
app.secret_key='Google authontification'
GOOGLE_CLIENT_ID = "1040310942524-g65htildicm86auusu7uk20pmptrfjc9.apps.googleusercontent.com"
client_secrets_file = os.path.join(pathlib.Path(__file__).parent,'client.json')

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=['https://www.googleapis.com/auth/userinfo.profile','https://www.googleapis.com/auth/userinfo.email','openid'],
    redirect_uri="http://127.0.0.1:5000/callback"
)

def login_required(function):
    def wrapper(*args, **kwargs):
        if 'google_id' not in session:
            return abort(401)
        else:
            return function()
    wrapper.__name__ = function.__name__
    return wrapper


heading = ' This heading looks epic ya zah'
content = """
Ywdi kol ma gole rah yakhlas el khadma
yzidolna fkin smana
w ana w delali fel jbel na7o f newwwaar
"""
db = list()

posts = 110
quantity = 6

for i in range(1,posts+1):
    heading_parts = heading.split()
    random.shuffle(heading_parts)
    content_parts = content.split()
    random.shuffle(content_parts)

    db.append([i,' '.join(heading_parts),' '.join(content_parts)])

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/login')
def log():
    authorization_url, state = flow.authorization_url()
    session['state'] = state
    return redirect(authorization_url)
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/work')
@login_required
def lazy():
    return render_template('lazy.html')


@app.route('/callback')
def callback():
    flow.fetch_token(authorization_response=request.url)
    if not session['state'] == request.args.get('state'):
        abort(500)
    credentials = flow.credentials
    request_session = requests.Session()
    cashed_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cashed_session)
    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID
    )
    session['google_id'] = id_info.get('sub')
    session['name'] = id_info.get('name')
    print(session['google_id'])
    return redirect('/work')


@app.route('/load')
def load():
    time.sleep(0.2)
    if request.args:
        if request.args.get('c'):

            try:
                counter = int(request.args.get('c'))
            except ValueError:
                return jsonify([])

            res= jsonify(db[counter:counter+quantity])
            return res
        else:
            return jsonify([])

    else:
        return jsonify([])


if __name__ == '__main__':
    app.run(port=5600)
