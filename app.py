from flask import Flask, request, abort
from flask import Flask

from linebot.exceptions import InvalidSignatureError

from settings import app, handler
from bot import handler


@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'
