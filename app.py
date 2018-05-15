from __future__ import unicode_literals

import errno
import os
import sys
import tempfile
from argparse import ArgumentParser
from collections import defaultdict
from random import randint
import sqlite3
from contextlib import closing

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


dbname = 'database.db'
with sqlite3.connect(dbname) as con:
    cur = con.cursor()
    try:
        cur.execute("create table shefs (display_name text, alias_name text, times integer)")
    except sqlite3.OperationalError:
        print("すでにデータベースが存在します。")

    con.commit()
    print("sqlite3の初期化")


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
    if ' ' in text and len(text.split(' ')) == 2:
        text_splited = text.split(' ')
    elif '　' in text and len(text.split('　')) == 2:
        text_splited = text.split(' ')

    try:
        display_name = line_bot_api.get_profile(event.source.user_id).display_name
    except linebot.exceptions.LineBotApiError:
        reply_message(event, '内部エラーデース')
        return


    if text == 'ヘルプ':
        reply_message(event,
            """'回数'　: 担当回数が見れるよ。
'任せろ': 料理は任せたぜ！
'シェフ': 今日のシェフを決めるよ。
'セット [数字]': 回数を設定
'エイリアス [名前]': 名前変更
'bye'  : グループから去ります。""")

    elif text == '回数':
        counter_str = ''
        with sqlite3.connect(dbname) as con:
            cur = con.cursor()
            for shef in cur.execute(f"select * from shefs"):
                if shef[1]:
                    counter_str += f"{shef[1]}: {shef[2]}\n"
                else:
                    counter_str += f"{shef[0]}: {shef[2]}\n"

        if counter_str == '':
            reply_message(event, 'シェフがいないようだ')
        else:
            reply_message(event, counter_str[:-1])

    elif text == '任せろ':
        rep_text = f"今日のシェフは{display_name}だ"
        with sqlite3.connect(dbname) as con:
            cur = con.cursor()
            shefs = list(cur.execute(f"select * from shefs where display_name = '{display_name}'"))
            if shefs and len(shefs) == 1:
                print(f"{shefs[0][0]}の回数は{shefs[0][2]}です。")
                cur.execute(f"update shefs set times = {shefs[0][2] + 1} where display_name = '{display_name}'")
                if shefs[0][1]:
                    rep_text = f"今日のシェフは{shefs[0][1]}だ"
            else:
                print('ないので作ります')
                cur.execute(f"insert into shefs values ('{display_name}', '', 1)")
            con.commit()

        if randint(0, 9) == 0:
            rep_text += '\n今日のご飯は上手くなるぞ！'
        reply_message(event, rep_text)

    elif text == 'シェフ':
        with sqlite3.connect(dbname) as con:
            cur = con.cursor()
            chefs_counter = cur.execute(f"select * from shefs")

        rep_text = 'シェフがいないようだ'
        if any(chefs_counter):
            shef = min(chefs_counter, key=lambda x: x[2])
            if shef[1]:
                rep_text = f'今日のシェフは{shef[1]}だ'
            else:
                rep_text = f'今日のシェフは{shef[0]}だ'
        reply_message(event, rep_text)

    elif text_splited[0] == 'セット':
        try:
            times = int(text_splited[1])
        except ValueError:
            reply_message(event, "ミス\nセット [数字]\nと入力してね")
            return

        with sqlite3.connect(dbname) as con:
            cur = con.cursor()
            shefs = list(cur.execute(f"select * from shefs where display_name = '{display_name}'"))
            if shefs and len(shefs) == 1:
                print(f"shefs: {shefs}")
                cur.execute(f"update shefs set times = {times} where display_name = '{display_name}'")
            else:
                print('ないので作ります')
                cur.execute(f"insert into shefs values ('{display_name}', '', {times})")
            con.commit()

        reply_message(event, "セットされたよ")

    elif text_splited[0] == 'エイリアス':
        try:
            alias_name = str(text_splited[1])
        except ValueError:
            reply_message(event, 'エラーですな')
            return

        with sqlite3.connect(dbname) as con:
            cur = con.cursor()
            shefs = list(cur.execute(f"select * from shefs where display_name = '{display_name}'"))
            if shefs and len(shefs) == 1:
                print(f"shefs: {shefs}")
                cur.execute(f"update shefs set alias_name = '{alias_name}' where display_name = '{display_name}'")
                reply_message(event, f"alias {alias_name} => {display_name}")
            else:
                reply_message(event, 'あなたはシェフではないな？')
            con.commit()

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
