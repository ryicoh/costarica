from costarica.chef import Chef
from costarica.reply.base import BaseCommand


class CountGetting(BaseCommand):
    def _execute_group(self):
        chefs_str = ''
        for chef in Chef.find_by_group(self._group_id):
            chefs_str += f'{chef.alias_name or chef.display_name}: {chef.times}回\n'

        if chefs_str == '':
            chefs_str = 'シェフがいないようだ'

        self._send_message(chefs_str.rstrip())

    def _execute_personal(self):
        chefs_str = ''
        for chef in Chef.find_by_user_id(self._user_id):
            chefs_str += f'[{chef.group_id}] {chef.alias_name or chef.display_name}: {chef.times}回\n'

        if chefs_str == '':
            chefs_str = '君は本当にシェフなのか？'

        self._send_message(chefs_str.rstrip())

    def _get_command_names(self):
        return ['回数', 'かいすう']


class CountSetting(BaseCommand):
    def _execute_group(self):
        try:
            times = int(self._argument)
        except ValueError:
            self._send_message('ミス\nセット [数字]\nと入力してね')
            return

        def create_chef():
            return Chef(self._display_name, times, self._group_id)

        chef = Chef.find_by_user_id_and_group_id(self._user_id, self._group_id, create_chef)
        chef.times = times
        chef.commit()

        self._send_message('成功！')

    def _get_command_names(self):
        return ['セット']
