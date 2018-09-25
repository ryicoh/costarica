from flask import request, abort
from linebot.exceptions import InvalidSignatureError

from costarica.bot import message_text
from costarica.settings import app, handler
import costarica.chef


@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)

    import json
    print(json.dumps(json.loads(body), indent=4))

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


@app.route("/")
def index():
    return "Welcome to Costarica!!"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

