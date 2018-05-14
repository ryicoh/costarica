from __future__ import unicode_literals

import errno
import os
import sys
import tempfile
from argparse import ArgumentParser
from collections import defaultdict
from random import randint

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    SourceUser, SourceGroup, SourceRoom,
    TemplateSendMessage, ConfirmTemplate, MessageTemplateAction,
    ButtonsTemplate, ImageCarouselTemplate, ImageCarouselColumn, URITemplateAction,
    PostbackTemplateAction, DatetimePickerTemplateAction,
    CarouselTemplate, CarouselColumn, PostbackEvent,
    StickerMessage, StickerSendMessage, LocationMessage, LocationSendMessage,
    ImageMessage, VideoMessage, AudioMessage, FileMessage,
    UnfollowEvent, FollowEvent, JoinEvent, LeaveEvent, BeaconEvent
)


app = Flask(__name__)

# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

chefs_counter = defaultdict(int)

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def message_text(event):
    text = event.message.text

    if text == 'ヘルプ':
        reply_message(event,
"""
'回数'　: みんなの担当回数が見れるよ。
'シェフ': 今日の当番は任せたぜ！
'bye'  : グループから去ります。
""")


    if text == '回数':
        message = ''
        for chef, count in chefs_counter:
            message += f"{chef}: {count}¥n"
        reply_message(event, message)

    elif text == 'シェフ':
        if isinstance(event.source, SourceUser):
            display_name = line_bot_api.get_profile(event.source.user_id).display_name
            reply_message(event, f"今日のシェフは{display_name}だ。")

            if randint(0, 10) == 0:
                reply_message(event, f"今日のご飯は上手くなるぞ！")

            chefs_counter[display_name] += 1

    elif text == 'bye':
        if isinstance(event.source, SourceGroup):
            reply_message(event, 'さらば')
            line_bot_api.leave_group(event.source.group_id)

        elif isinstance(event.source, SourceRoom):
            reply_message(event, 'さらば')

        else:
            reply_message(event, "個人チャットでは退出できなのだ")


def reply_message(event, message):
    line_bot_api.reply_message(
        event.reply_token, [TextSendMessage(text=message)]
    )


if __name__ == "__main__":
    arg_parser = ArgumentParser(
        usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
    )
    arg_parser.add_argument('-p', '--port', default=8000, help='port')
    arg_parser.add_argument('-d', '--debug', default=False, help='debug')
    options = arg_parser.parse_args()

    app.run(debug=options.debug, port=options.port)
