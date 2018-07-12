import os

from flask import Flask, request, abort
from flask_sqlalchemy import SQLAlchemy
from linebot import LineBotApi, WebhookHandler


app = Flask(__name__)

# Postgresql
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', None) or \
                                        "postgresql://localhost/costarica"
db = SQLAlchemy(app)

# Line Bot API
channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)

if channel_secret is None or channel_access_token is None:
    raise EnvironmentError('Specify LINE_CHANNEL_SECRET as environment variable.')

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)
