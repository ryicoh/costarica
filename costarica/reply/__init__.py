from costarica.reply.cook import TodayChef, TodayChefChoice, ChefAlias
from costarica.reply.info import Info, Removal
from costarica.reply.time import CountGetting, CountSetting

reply_list = [
    TodayChef(), TodayChefChoice(), ChefAlias(),
    Info(), Removal(),
    CountGetting(), CountSetting()
]
