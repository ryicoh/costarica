from abc import ABCMeta, abstractmethod

from linebot.exceptions import LineBotApiError
from linebot.models import (
    TextSendMessage, SourceUser,
    SourceGroup, SourceRoom
)

from costarica.line import line_bot_api


class BaseCommand(metaclass=ABCMeta):

    def __init__(self):
        self._argument = None
        self._event = None
        self._user_id = None
        self._group_id = None
        self._group_name = None
        self._display_name = None

    def execute(self, event, command_name, argument):
        if command_name not in self._get_command_names():
            return
 
        self._event = event
        self._argument = argument
        self._user_id = event.source.user_id

        if isinstance(self._event.source, SourceRoom):
            self._send_message('すまぬぅ！ \nルームには対応していません。')
            return

        try:
            self._display_name = line_bot_api.get_profile(
                                     self._user_id).display_name
        except LineBotApiError:
            self._send_message('CostaRicaをともだちに追加してね。')
            return

        if isinstance(self._event.source, SourceUser):
            self._execute_personal()

        elif isinstance(self._event.source, SourceGroup):
            self._group_id = event.source.group_id
            self._execute_group()

    @abstractmethod
    def _execute_group(self):
        raise NotImplemented()

    def _execute_personal(self):
        pass

    @abstractmethod
    def _get_command_names(self) -> list:
        raise NotImplemented()

    def _send_message(self, text):
        line_bot_api.reply_message(
            self._event.reply_token, [TextSendMessage(text=text)])
