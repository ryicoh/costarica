from random import randint

from .base import BaseCommand
from ..chef import Chef


class TodayChef(BaseCommand):
    def _execute(self):
        def create_chef():
            return Chef(self._display_name, 0, self._group_id)

        chef = Chef.find_by_name(self._group_id, self._display_name, create_chef)
        chef.times += 1
        chef.commit()

        rep_text = f'今日のシェフは{chef.alias_name or chef.name}だ'

        if randint(0, 9) == 0:
            rep_text += '\n今日のご飯は上手くなるぞ！'
        self._send_message(rep_text)

    def _get_command_name(self):
        return ['任せろ', 'まかせろ', '俺がやるぜ']


class TodayChefChoice(BaseCommand):
    def _execute(self):
        chefs = Chef.find_by_group(self._group_id)
        text = 'シェフがいないようだ'
        if chefs:
            today_chef = min(chefs, key=lambda chef: chef.times)
            text = today_chef.alias_name or today_chef.name
        self._send_message(text)

    def _get_command_name(self):
        return ['シェフだれ', 'シェフだれ?', 'シェフだれ？',
                'シェフ誰', 'シェフ誰?', 'シェフ誰？']


class ChefAlias(BaseCommand):
    def _execute(self):
        try:
            alias_name = str(self._argument)
        except ValueError:
            self._send_message('エラーですな')
            return

        def not_found():
            self._send_message('シェフではないな？')

        chef = Chef.find_by_name(self._group_id, self._display_name, not_found)
        chef.alias_name = alias_name
        chef.commit()

        self._send_message(f'{alias_name}とお呼びしますね！')

    def _get_command_name(self):
        return ['エイリアス', 'alias']
