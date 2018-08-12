import os
from random import randint

from linebot.exceptions import LineBotApiError

from linebot.models import (
    MessageEvent, TextMessage,
    TextSendMessage, SourceGroup,
    SourceRoom
)

from settings import line_bot_api, handler
from shef import Shef


@handler.add(MessageEvent, message=TextMessage)
def message_text(event):
    cmd, arg = split_text(event.message.text)

    try:
        display_name = line_bot_api.get_profile(event.source.user_id).display_name
    except LineBotApiError:
        reply_message(event, 'CostaRicaをともだちに追加してね。')
        return

    try:
        group_id = event.source.group_id
    except LineBotApiError:
        reply_message(event, 'グループIDが取得できません。')
        return


    if cmd == 'ヘルプ':
        reply_message(event, \
"""'回数'　: 担当回数が見れるよ。
'任せろ': 料理は任せたぜ！
'シェフ': 今日のシェフを決めるよ。
'セット [数字]': 回数を設定
'エイリアス [名前]': 名前変更
'bye'  : グループから去ります。"""
        )

    elif cmd == '回数':
        shefs_str = ''
        for shef in Shef.find_by_group(group_id):
            shefs_str += f'{shef.alias_name or shef.name}: {shef.times}回\n'

        if shefs_str == '':
            reply_message(event, 'シェフがいないようだ')
        else:
            reply_message(event, shefs_str[:-1])

    elif cmd == '任せろ':
        def create_shef():
            return Shef(display_name, 0, group_id)

        shef = Shef.find_by_name(group_id, display_name, create_shef)
        shef.times += 1
        shef.commit()

        rep_text = f"今日のシェフは{shef.alias_name or shef.name}だ"

        if randint(0, 9) == 0:
            rep_text += '\n今日のご飯は上手くなるぞ！'
        reply_message(event, rep_text)

    elif cmd == 'シェフ':
        shefs = Shef.find_by_group(group_id)
        rep_text = 'シェフがいないようだ'
        if shefs:
            todays_shef = min(shefs, key=lambda shef: shef.times)
            rep_text = todays_shef.alias_name or todays_shef.name
        reply_message(event, rep_text)

    elif cmd == 'セット':
        try:
            times = int(arg)
        except ValueError:
            reply_message(event, "ミス\nセット [数字]\nと入力してね")
            return

        def create_shef():
            return Shef(display_name, times, group_id)

        shef = Shef.find_by_name(group_id, display_name, create_shef)
        shef.times = times
        shef.commit()

        reply_message(event, "成功！")

    elif cmd == 'エイリアス':
        try:
            alias_name = str(arg)
        except ValueError:
            reply_message(event, 'エラーですな')
            return

        def notfound():
            reply_message(event, "シェフではないな？")

        shef = Shef.find_by_name(group_id, display_name, notfound)
        shef.alias_name = alias_name
        shef.commit()
        reply_message(event, f"alias {alias_name} => {display_name}")

    elif cmd == 'bye':
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

def split_text(text):
    seps = [' ', '　']
    for sep in seps:
        text_splited = text.split(sep)
        if len(text_splited) == 2:
            return text_splited

    return text, ''
