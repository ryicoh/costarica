from linebot.models import MessageEvent, TextMessage

from costarica.line import handler
from costarica.reply import reply_list


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
