from .base import BaseCommand
from ..chef import Chef


class CountGetting(BaseCommand):
    def _execute(self):
        chefs_str = ''
        for chef in Chef.find_by_group(self._group_id):
            chefs_str += f'{chef.alias_name or chef.name}: {chef.times}回\n'

        if chefs_str == '':
            self._send_message('シェフがいないようだ')
        else:
            self._send_message(chefs_str.rstrip())

    def _get_command_name(self):
        return "回数"


class CountSetting(BaseCommand):
    def _execute(self):
        try:
            times = int(self._argument)
        except ValueError:
            self._send_message("ミス\nセット [数字]\nと入力してね")
            return

        def create_chef():
            return Chef(self._display_name, times, self._group_id)

        chef = Chef.find_by_name(self._group_id, self._display_name, create_chef)
        chef.times = times
        chef.commit()

        self._send_message("成功！")

    def _get_command_name(self):
        return "セット"
