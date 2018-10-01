import os

from linebot import LineBotApi, WebhookHandler


channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
assert channel_secret, 'Specify LINE_CHANNEL_SECRET as environment variable.'

channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
assert channel_access_token, 'Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.'

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)
