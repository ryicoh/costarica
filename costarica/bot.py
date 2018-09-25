from linebot.models import MessageEvent, TextMessage

from costarica.settings import handler
from costarica.reply import info, cook, time

reply_list = [
    time.CountGetting(),
    time.CountSetting(),
    cook.TodayChef(),
    cook.TodayChefChoice(),
    cook.ChefAlias(),
    info.Info(),
    info.Removal(),
]


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
