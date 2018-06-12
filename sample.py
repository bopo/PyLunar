import datetime
import traceback

from pylunar import Converter, DateNotExist, Lunar, Solar
from pylunar.festival import festivals
from pylunar.solarterm import solarterms

# 公历转农历:
solar = Solar(2018, 1, 1)
print(solar)
lunar = Converter.Solar2Lunar(solar)
print(lunar)
solar = Converter.Lunar2Solar(lunar)
print(solar)
print(solar.to_date(), type(solar.to_date()))

# 农历转公历:

lunar = Lunar(2018, 2, 30, isleap=False)
print(lunar)
solar = Converter.Lunar2Solar(lunar)
print(solar)
lunar = Converter.Solar2Lunar(solar)
print(lunar)
print(lunar.to_date(), type(lunar.to_date()))
print(Lunar.from_date(datetime.date(2018, 4, 15)))


# # 日期合法性检查, 农历和公历都起作用, 如: 农历闰月2018-2-15是不存在的，但农历闰月2012-4-4是存在的:

Lunar(2012, 4, 4, isleap=True)  # date(2012, 5, 24)

try:
    lunar = Lunar(2018, 2, 15, isleap=False)
except DateNotExist:
    print(traceback.format_exc())


for x in [(f(2018), f.get_lang('zh')) for f in sorted(solarterms, key=lambda _f: _f(20 18))]:
    print('{} {}'.format(*x))

# # 打印收录的节假日, 支持中文、英文输出，其他语言需要扩展(欢迎fork & pull-request):

# print festivals, using English or Chinese
# print("----- print all festivals on 2018 in chinese: -----")
# for fest in festivals:
#     print(fest.get_lang('zh'), fest(2018))

# print("----- print all festivals on 2017 in english: -----")
# for fest in festivals:
#     print(fest.get_lang('en'), fest(2017))    
