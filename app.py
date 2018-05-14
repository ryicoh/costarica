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
    nonlocal display_name

    text = event.message.text
    if isinstance(event.source, SourceUser):
        print(f"ユーザーIDは{event.source.user_id}です")
        display_name = line_bot_api.get_profile(event.source.user_id).display_name
    else:
        reply_message(event, 'User IDを設定してね')
        return

    if text == 'ヘルプ':
        reply_message(event,
            """'回数'　: 担当回数が見れるよ。
'任せろ': 料理は任せたぜ！
'シェフ': 今日のシェフを決めるよ。
'セット [数字]': 回数を設定
'bye'  : グループから去ります。""")

    elif text == '回数':
        if chefs_counter:
            counter_str = ''
            for chef, count in chefs_counter.items():
                counter_str += f"{chef}: {count}\n"
            reply_message(event, counter_str)

        else:
            reply_message(event, 'シェフがいないようだ')


    elif text == '任せろ':
        reply_message(event, f"今日のシェフは{display_name}だ")

        if randint(0, 10) == 0:
            reply_message(event, f"今日のご飯は上手くなるぞ！")

        print("実行前: ", end='')
        print(chefs_counter[display_name])
        chefs_counter[display_name] += 1
        print("実行後: ", end='')
        print(chefs_counter[display_name])

    elif text == 'シェフ':
        if chefs_counter:
            reply_message(event, f'今日のシェフは{min(chefs_counter.items(), key=lambda x:x[1])[0]}だ')
        else:
            reply_message(event, 'シェフがいないようだ')

    elif text.split(' ')[0] == 'セット':
        try:
            chefs_counter[display_name] = int(text.split(' ')[1])
            reply_message(event, "セットされたよ")
        except ValueError:
            reply_message(event, "ミス\nセット　[数字]\nと入力してね")

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
