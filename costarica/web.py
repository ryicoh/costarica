from flask import Flask
from flask import request, abort
from linebot.exceptions import InvalidSignatureError

from costarica.line import handler


app = Flask(__name__)


@app.route('/')
def index():
    return 'Welcome to Costarica!!'


@app.route('/callback', methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'
