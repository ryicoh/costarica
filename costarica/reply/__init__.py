from .cook import TodayChef, TodayChefChoice, ChefAlias
from .info import Info, Removal
from .time import CountGetting, CountSetting

reply_list = [
    TodayChef(), TodayChefChoice(), ChefAlias(),
    Info(), Removal(),
    CountGetting(), CountSetting()
]
