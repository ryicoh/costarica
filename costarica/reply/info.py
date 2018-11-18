from linebot.models import SourceGroup, SourceRoom

from costarica.line import line_bot_api
from costarica.reply.base import BaseCommand
import textwrap


class Info(BaseCommand):
    def _execute_group(self):
        text = """
            '回数'　: 担当回数が見れるよ
            '任せろ': 掃除は任せたぜ！
            '今日の当番は？': 今日の当番決め
            'セット [数字]': 回数を設定
            'エイリアス [名前]': 名前変更
            'bye'  : グループから去ります
        """

        text = textwrap.dedent(text).strip()
        self._send_message(text)

    def _execute_personal(self):
        text = """
            '回数'　: 担当回数が見れるよ
        """
        text = textwrap.dedent(text).strip()
        self._send_message(text)

    def _get_command_names(self):
        return ['ヘルプ', 'へるぷ', 'help']


class Removal(BaseCommand):
    def _execute_group(self):
        if isinstance(self._event.source, SourceGroup):
            self._send_message('さようなら〜\nまた会えるといいね。')
            line_bot_api.leave_group(self._event.source.group_id)

        elif isinstance(self._event.source, SourceRoom):
            self._send_message('さらば')
            line_bot_api.leave_room(self._event.source.group_id)

    def _execute_personal(self):
        self._send_message('個人チャットでは退出できなのだ')

    def _get_command_names(self):
        return ['bye']
