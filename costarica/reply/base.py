from abc import ABCMeta, abstractmethod

from linebot.exceptions import LineBotApiError
from linebot.models import TextSendMessage

from costarica.settings import line_bot_api


class BaseCommand(metaclass=ABCMeta):

    def __init__(self):
        self._argument = None
        self._event = None
        self._group_id = None
        self._display_name = None

    def execute(self, event, command_name, argument):
        _command_name = self._get_command_name()

        if type(_command_name) == str and command_name != _command_name:
            return

        if type(_command_name) and command_name not in _command_name:
            return
 
        self._event = event
        self._argument = argument
        try:
            self._display_name = line_bot_api.get_profile(event.source.user_id).display_name
        except LineBotApiError:
            self._send_message('CostaRicaをともだちに追加してね。')
            return

        try:
            self._group_id = event.source.group_id
        except LineBotApiError:
            self._send_message(event, 'グループIDが取得できません。')
            return

        self._execute()

    @abstractmethod
    def _execute(self):
        raise NotImplemented()

    @abstractmethod
    def _get_command_name(self):
        raise NotImplemented()

    def _send_message(self, text):
        line_bot_api.reply_message(
            self._event.reply_token, [TextSendMessage(text=text)])
