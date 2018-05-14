import os
import sys
from argparse import ArgumentParser

from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)




def main(options):
    global __name__

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

    app.run(debug=options.debug, port=options.port)


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

    print(dir(event))
    print(dir(message))

    if text == 'profile':
        if isinstance(event.source, SourceUser):
            profile = line_bot_api.get_profile(event.source.user_id)
            line_bot_api.reply_message(
                event.reply_token, [
                    TextSendMessage(
                        text='Display name: ' + profile.display_name
                    ),
                    TextSendMessage(
                        text='Status message: ' + profile.status_message
                    )
                ]
            )
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextMessage(text="Bot can't use profile API without user ID"))
    elif text == 'bye':
        if isinstance(event.source, SourceGroup):
            line_bot_api.reply_message(
                event.reply_token, TextMessage(text='Leaving group'))
            line_bot_api.leave_group(event.source.group_id)
        elif isinstance(event.source, SourceRoom):
            line_bot_api.reply_message(
                event.reply_token, TextMessage(text='Leaving group'))
            line_bot_api.leave_room(event.source.room_id)
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextMessage(text="Bot can't leave from 1:1 chat"))
    elif text == 'confirm':
        confirm_template = ConfirmTemplate(text='Do it?', actions=[
            MessageTemplateAction(label='Yes', text='Yes!'),
            MessageTemplateAction(label='No', text='No!'),
        ])
        template_message = TemplateSendMessage(
            alt_text='Confirm alt text', template=confirm_template)
        line_bot_api.reply_message(event.reply_token, template_message)
    elif text == 'buttons':
        buttons_template = ButtonsTemplate(
            title='My buttons sample', text='Hello, my buttons', actions=[
                URITemplateAction(
                    label='Go to line.me', uri='https://line.me'),
                PostbackTemplateAction(label='ping', data='ping'),
                PostbackTemplateAction(
                    label='ping with text', data='ping',
                    text='ping'),
                MessageTemplateAction(label='Translate Rice', text='米')
            ])
        template_message = TemplateSendMessage(
            alt_text='Buttons alt text', template=buttons_template)
        line_bot_api.reply_message(event.reply_token, template_message)
    elif text == 'carousel':
        carousel_template = CarouselTemplate(columns=[
            CarouselColumn(text='hoge1', title='fuga1', actions=[
                URITemplateAction(
                    label='Go to line.me', uri='https://line.me'),
                PostbackTemplateAction(label='ping', data='ping')
            ]),
            CarouselColumn(text='hoge2', title='fuga2', actions=[
                PostbackTemplateAction(
                    label='ping with text', data='ping',
                    text='ping'),
                MessageTemplateAction(label='Translate Rice', text='米')
            ]),
        ])
        template_message = TemplateSendMessage(
            alt_text='Carousel alt text', template=carousel_template)
        line_bot_api.reply_message(event.reply_token, template_message)
    elif text == 'image_carousel':
        image_carousel_template = ImageCarouselTemplate(columns=[
            ImageCarouselColumn(image_url='https://via.placeholder.com/1024x1024',
                                action=DatetimePickerTemplateAction(label='datetime',
                                                                    data='datetime_postback',
                                                                    mode='datetime')),
            ImageCarouselColumn(image_url='https://via.placeholder.com/1024x1024',
                                action=DatetimePickerTemplateAction(label='date',
                                                                    data='date_postback',
                                                                    mode='date'))
        ])
        template_message = TemplateSendMessage(
            alt_text='ImageCarousel alt text', template=image_carousel_template)
        line_bot_api.reply_message(event.reply_token, template_message)
    elif text == 'imagemap':
        pass
    else:
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=event.message.text))



if __name__ == "__main__":
    arg_parser = ArgumentParser(
        usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
    )
    arg_parser.add_argument('-p', '--port', default=8000, help='port')
    arg_parser.add_argument('-d', '--debug', default=False, help='debug')
    options = arg_parser.parse_args()
    main(options)
