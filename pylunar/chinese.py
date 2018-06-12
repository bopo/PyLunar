from ._era import BOUGHS, LUNAR_DAY, LUNAR_MON, TRUNKS, ZODIAC


def LunarString(lunar, embolism=False):
    # 生成属相
    lsx = ((lunar.year - 4) % 60) % 12
    
    if lsx < 0 or lsx >= len(ZODIAC):
        raise ValueError('Error Year for Shuxiang')

    sShuxiang = ZODIAC[lsx]

    # 生成农历天干
    nTianGan = ((lunar.year - 4) % 60) % 10
    
    if nTianGan < 0 or nTianGan >= len(TRUNKS):
        raise ValueError('Error Year for TianGan')
    
    sTianGan = TRUNKS[nTianGan]
    
    # 生成地支
    nDiZhi = ((lunar.year - 4) % 60) % 12
    
    if nDiZhi < 0 or nDiZhi >= len(BOUGHS):
        raise ValueError('Error Year for Dizhi')
    
    sDiZhi = BOUGHS[nDiZhi]
    
    # 生成农历月
    if lunar.month < 0 or lunar.month >= len(LUNAR_MON):
        raise ValueError('Error Month for LunMonth')
    
    sNongliMonth = LUNAR_MON[lunar.month]
    
    if embolism:
        sNongliMonth = '闰' + sNongliMonth

    # 生成农历日
    if lunar.day < 0 or lunar.day >= len(LUNAR_DAY):
        raise ValueError('Error Month for LunDay')
    
    sNongliDay = LUNAR_DAY[lunar.day]

    return sShuxiang, sTianGan, sDiZhi, sNongliMonth, sNongliDay
    # return {
    #     'sx': sShuxiang,
    #     'tg': sTianGan,
    #     'dz': sDiZhi,
    #     'month': sNongliMonth,
    #     'day': sNongliDay,
    # }



def LunarEra(lunar, hour=None, minute=None):
    # (lunar.year, lunar.month, lunar.day, hour, minute) = xxx_todo_changeme4
    (sShuxiang, sTianGan, sDiZhi, sNongliMonth, sNongliDay) = LunarString(lunar, True)
    
    nTianGan = ((lunar.year - 4) % 60) % 10
    
    # 时辰
    nShiCheng = int(hour / 2)
    
    if hour % 2 == 1:  # [a<=x<b)半开半闭
        nShiCheng += 1
    
    if nShiCheng == 12:
        nShiCheng = 0
    
    # 分钟
    nMinute = int(minute / 10)
    
    if hour % 2 == 0:
        nMinute += 6  # 1'分'含120分钟

    # 年干支
    str_Year = sTianGan + sDiZhi
    # 月干支
    cListMonth = settings.cListMonth

    # 天干名称
    cTianGan = settings.cTianGan
    # 地支名称
    cDizhi = settings.cDizhi

    (sFeast, nFeastMonth) = Get24LunarFeast((lunar.year, lunar.month, lunar.day))
    nMonth = nFeastMonth  # 二十四节气定年月支

    if lunar.month == 12:
        if nFeastMonth == 13:
            nMonth = 1

            for nTG in range(0, 10):
                if sTianGan == cTianGan[nTG]:
                    sTianGan = cTianGan[(nTG - 1) % 10]
                    break

            for nDZ in range(0, 12):
                if sDiZhi == cDizhi[nDZ]:
                    sDiZhi = cDizhi[(nDZ - 1) % 12]
                    break

        # if nFeastMonth == 13:
        #     nMonth = 1

    if nTianGan >= 5:
        nTianGan -= 5
    
    str_Month = cListMonth[nMonth - 1][nTianGan]
    # 日干支
    # 1.求元旦干支 以阳历日期来求
    nGongYuanYear = lunar.year % 100  # 公元纪年的最后两位
    
    if nGongYuanYear == 0:
        nGongYuanYear = 100  # 百年逢百
    
    nA = (nGongYuanYear % 12) * 5
    nB = int(nGongYuanYear / 4)

    if not nGongYuanYear % 4 == 0:
        nB = nB + 1
    
    nYuanDanGanZHi = nA + nB
    # 2.查表 以cListMonth排列
    # 1901～2000年间以甲戌作1向后推某年C的值，既是该年元旦的干支﹙2001～2100年间以己未作1﹚
    nGongYuan = lunar.year
    
    nX = int(nYuanDanGanZHi / 12) % 5
    nY = nYuanDanGanZHi % 12
    
    if nGongYuan > 2000:
        nX = (nX + 4) % 5
    
        if nY + 5 > 12:
            nX = (nX + 1) % 5
    
        nY = (nY + 4) % 12
    
    if nGongYuan <= 2000:
        if nY + 8 > 12:
            nX = (nX + 1) % 5
    
        nY = (nY + 7) % 12
    
    str_YuanDanDay = cListMonth[nY][nX]
    # 3.求当日干支
    nDayGan, nDayZhi = 0, 0

    for n in range(0, 10):
        if str_YuanDanDay[:1] == cTianGan[n]:  # C源码中文为两个字节，Python为一个
            nDayGan = n
            break

    for k in range(0, 12):
        if str_YuanDanDay[1:] == cDizhi[k]:
            nDayZhi = k
            break

    # 诗诀
    # 一月干支均减１    二月干加０支加６   三月干减二支加10
    # 四月干减１支加５  五月干支均减１     六月干加０支加６
    # 七月干支均加０    八月干加１支加７   九月干支均加２ 　
    # 十月干加２支加８  十一月干支均加３ 　十二月干加３支加９
    nGanRun, nZhiRun = 0, 0

    if lunar.month == 1:
        nGanRun = nGanRun - 1
        nZhiRun = nZhiRun - 1
    elif lunar.month == 2:
        nZhiRun = nZhiRun + 6
    elif lunar.month == 3:
        nGanRun = nGanRun - 2
        nZhiRun = nZhiRun + 10
    elif lunar.month == 4:
        nGanRun = nGanRun - 1
        nZhiRun = nZhiRun + 5
    elif lunar.month == 5:
        nGanRun = nGanRun - 1
        nZhiRun = nZhiRun - 1
    elif lunar.month == 6:
        nZhiRun += 6
    elif lunar.month == 8:
        nGanRun += 1
        nZhiRun += 7
    elif lunar.month == 9:
        nGanRun += 2
        nZhiRun += 2
    elif lunar.month == 10:
        nGanRun += 2
        nZhiRun += 8
    elif lunar.month == 11:
        nGanRun += 3
        nZhiRun += 3
    elif lunar.month == 12:
        nGanRun += 3
        nZhiRun += 9

    nRunYear = 0

    # 四年一闰,百年不闰,四百年再闰
    if (lunar.year %
        400 == 0) or (not lunar.year %
                      100 == 0) and (lunar.year %
                                     4 == 0):
        if lunar.month > 2:
            nRunYear += 1

    cListTime = settings.cListTime
    # (nDayGan）+（nDay）+（所求月的天干加减数、闰年三月以后减1）÷10
    nTodayGan = (nDayGan + lunar.day + nGanRun + nRunYear) % 10
    #（所求年份的元旦地支）+（所求日期）+（所求月的地支加减数、闰年三月以后减1）÷12
    nTodayZhi = (nDayZhi + lunar.day + nZhiRun + nRunYear) % 12

    str_TodayGan = cTianGan[nTodayGan]
    str_TodayZhi = cDizhi[nTodayZhi]
    
    str_Day = str_TodayGan + str_TodayZhi
    
    #//时干支
    str_Time = cListTime[nShiCheng][int(nTodayGan % 5)]
    nTimeGan = 0 # 考刻分 时上起刻

    for j in range(0, 10):
        if str_Time[:1] == cTianGan[j]:
            nTimeGan = j
            break
    
    str_Minute = cListTime[nMinute][int(nTimeGan % 5)]

    # 四柱 + 考时 + 十字
    return str_Year, str_Month, str_Day, str_Time, str_Minute
