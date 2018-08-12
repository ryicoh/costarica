import os
import socket

from flask import Flask, request, abort
from flask_sqlalchemy import SQLAlchemy
from linebot import LineBotApi, WebhookHandler


app = Flask(__name__)

def is_ipv6(addr):
    """Checks if a given address is an IPv6 address."""
    try:
        socket.inet_pton(socket.AF_INET6, addr)
        return True
    except socket.error:
        return False


app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI', None)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

assert app.config['SQLALCHEMY_DATABASE_URI'], 'Specify SQLALCHEMY_DATABASE_URI as environment variable.'

db = SQLAlchemy(app)

# Line Bot API
channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
assert channel_secret, 'Specify LINE_CHANNEL_SECRET as environment variable.'

channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
assert channel_access_token, 'Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.'


line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)
