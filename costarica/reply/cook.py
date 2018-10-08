from random import randint

from costarica.reply.base import BaseCommand
from costarica.chef import Chef


class TodayChef(BaseCommand):
    def _execute_group(self):
        def create_chef():
            return Chef(self._user_id, self._display_name, 0,
                        group_id=self._group_id)

        chef = Chef.find_by_user_id_and_group_id(self._user_id,
                                                 self._group_id, create_chef)
        chef.times += 1
        chef.commit()

        rep_text = f'今日のシェフは{chef.alias_name or chef.display_name}だ'

        if randint(0, 9) == 0:
            rep_text += '\n今日のご飯は上手くなるぞ！'
        self._send_message(rep_text)

    def _get_command_names(self):
        return ['任せろ', 'まかせろ', '俺がやるぜ']


class TodayChefChoice(BaseCommand):
    def _execute_group(self):
        chefs = Chef.find_by_group(self._group_id)
        text = 'メンバーがいないようだ'
        if chefs:
            today_chef = min(chefs, key=lambda chef: chef.times)
            text = today_chef.alias_name or today_chef.display_name
        self._send_message(text)

    def _get_command_names(self):
        return ['今日の当番は？', '今日の当番は?', '当番だれ？', '当番だれ?',
                '当番誰？', '当番誰?', '当番は誰？', '当番は誰?',
                '当番だーれ？', '当番だーれ?', '当番はだーれ？', '当番はだーれ?',
                '当番だあれ？', '当番だあれ?', '当番はだあれ？', '当番はだあれ?',
                '今日の当番は', '当番だれ', '当番誰', '当番は誰',
                '当番はだーれ', '当番はだあれ']


class ChefAlias(BaseCommand):
    def _execute_group(self):
        try:
            alias_name = str(self._argument)
        except ValueError:
            self._send_message('エラーですな')
            return

        def not_found():
            self._send_message('メンバーではないな？')

        chef = Chef.find_by_user_id_and_group_id(self._user_id,
                                                 self._group_id, not_found)
        if chef is None:
            return

        chef.alias_name = alias_name
        chef.commit()

        self._send_message(f'{alias_name}とお呼びしますね！')

    def _get_command_names(self):
        return ['エイリアス', 'alias']
