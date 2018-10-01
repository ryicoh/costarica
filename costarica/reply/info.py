from linebot.models import SourceGroup, SourceRoom

from ..linebot import line_bot_api
from .base import BaseCommand
import textwrap


class Info(BaseCommand):
    def _execute(self):
        text = """
            '回数'　: 担当回数が見れるよ
            '任せろ': 料理は任せたぜ！
            'シェフだれ？': 今日のシェフ決め
            'セット [数字]': 回数を設定
            'エイリアス [名前]': 名前変更
            'bye'  : グループから去ります
        """

        text = textwrap.dedent(text).strip()
        self._send_message(text)

    def _get_command_name(self):
        return ['ヘルプ', 'へるぷ', 'help']


class Removal(BaseCommand):
    def _execute(self):
        text = '個人チャットでは退出できなのだ'
        if isinstance(self._event.source, SourceGroup):
            text = 'さようなら〜\nまた会えるといいね。'
            line_bot_api.leave_group(self._event.source.group_id)

        elif isinstance(self._event.source, SourceRoom):
            text = 'さらば'
            line_bot_api.leave_room(self._event.source.group_id)

        self._send_message(text)

    def _get_command_name(self):
        return ['bye']
