import os

from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage

from .reply import reply_list


channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
assert channel_secret, 'Specify LINE_CHANNEL_SECRET as environment variable.'

channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
assert channel_access_token, 'Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.'


line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)


@handler.add(MessageEvent, message=TextMessage)
def message_text(event):
    command, argument = _split_text(event.message.text)

    for reply in reply_list:
        reply.execute(event, command, argument)


def _split_text(text):
    seps = [' ', '　']
    for sep in seps:
        texts = text.split(sep)
        if len(texts) == 2:
            return texts

    return text, ''
