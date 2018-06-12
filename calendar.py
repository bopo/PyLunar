
# 公历转农历
import datetime

import settings


def Gregorian2Lunar(xxx_todo_changeme):
    # 公历每月前面的天数
    (wCurYear, wCurMonth, wCurDay) = xxx_todo_changeme
    
    # wMonthAdd = (0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334)
    wMonthAdd = settings.wMonthAdd
    wLunarData = settings.wNongliData

    # 农历数据
    wNongliData = settings.wNongliData

    # 取当前公历年、月、日
    #year,month,day = GregorianDate.split('-')
    # wCurYear,wCurMonth,wCurDay=int(year),int(month),int(day)
    wLunarYear, wLunarMonth, wLunarDay = None, None, None
    
    # 计算到初始时间1901年2月19日的天数：1921-2-19(正月初一)
    nTheDate = (wCurYear - 1901) * 365 + (wCurYear - 1901) / \
        4 + wCurDay + wMonthAdd[wCurMonth - 1] - 38 - 11
    
    if nTheDate <= 0:
        return None, None, None
    
    # 闰年
    if (not wCurYear % 4) and (wCurMonth > 2):
        nTheDate = nTheDate + 1
    
    # 计算农历天干、地支、月、日
    nIsEnd = False
    m = 0
    
    while not nIsEnd:
        # if wNongliData[m] < 4095:
        #     k = 11
        # else:
        #     k = 12

        k = 11 if wNongliData[m] < 4095 else 12        
        n = k

        while n >= 0:
            nBit = wNongliData[m]

            for i in range(1, n + 1, 1):
                nBit = nBit / 2
            
            nBit = nBit % 2

            if nTheDate <= (29 + nBit):
                nIsEnd = True
                break

            nTheDate = nTheDate - 29 - nBit
            n = n - 1
        
        if nIsEnd:
            break

        m = m + 1

    wCurMonth = k - n + 1
    wCurYear  = 1901 + m
    wCurDay   = nTheDate

    if wCurDay < 0:
        return None, None, None

    if k == 12:
        if wCurMonth == wNongliData[m] / 65536 + 1:
            wCurMonth = 1 - wCurMonth
        elif wCurMonth > wNongliData[m] / 65536 + 1:
            wCurMonth = wCurMonth - 1

    wLunarYear = wCurYear
    Embolism = False  # 闰月

    if wCurMonth < 1:
        wLunarMonth = -wCurMonth
        Embolism = True
    else:
        wLunarMonth = wCurMonth
        Embolism = False
    
    wLunarDay = wCurDay
    
    return wLunarYear, wLunarMonth, wLunarDay, Embolism

# 农历转公历
def Lunar2Gregorian(xxx_todo_changeme1):
    # 取当前公历年、月、日
    #year,month,day = LunarDate.split('-')
    # wCurYear,wCurMonth,wCurDay=int(year),int(month),int(day)
    (nLunYear, nLunMonth, nLunDay, bEmbolism) = xxx_todo_changeme1
    tStart = datetime.date(nLunYear, nLunMonth, nLunDay)
    tSpan = datetime.timedelta(days=1)

    for i in range(0, 101):
        wLunYear, wLunMonth, wLunDay, wEmbolism = Gregorian2Lunar(
            (tStart.year, tStart.month, tStart.day))
    
        if wLunYear == nLunYear and wLunMonth == nLunMonth and wLunDay == nLunDay and bEmbolism == wEmbolism:
            return tStart.year, tStart.month, tStart.day
    
        tStart += tSpan
    
    return None, None, None


def GetLunarString(xxx_todo_changeme2):
    # 天干名称
    (nLunYear, nLunMonth, nLunDay, bEmbolism) = xxx_todo_changeme2
    # cTianGan = ("甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸")
    cTianGan = settings.cTianGan
    # 地支名称
    cDizhi = settings.cDizhi

    # 属相名称
    cShuxiang = settings.cShuxiang

    # 农历日期名
    cDayName = settings.cDayName

    # 农历月份名
    cMonName = settings.cMonName

    # 生成属相
    nShuXiang = ((nLunYear - 4) % 60) % 12
    
    if nShuXiang < 0 or nShuXiang >= len(cShuxiang):
        raise ValueError('Error Year for Shuxiang')

    sShuxiang = cShuxiang[nShuXiang]

    # 生成农历天干
    nTianGan = ((nLunYear - 4) % 60) % 10
    
    if nTianGan < 0 or nTianGan >= len(cTianGan):
        raise ValueError('Error Year for TianGan')
    
    sTianGan = cTianGan[nTianGan]
    
    # 生成地支
    nDiZhi = ((nLunYear - 4) % 60) % 12
    
    if nDiZhi < 0 or nDiZhi >= len(cDizhi):
        raise ValueError('Error Year for Dizhi')
    
    sDiZhi = cDizhi[nDiZhi]
    
    # 生成农历月
    if nLunMonth < 0 or nLunMonth >= len(cMonName):
        raise ValueError('Error Month for LunMonth')
    
    sNongliMonth = cMonName[nLunMonth] + '月'
    
    if bEmbolism:
        sNongliMonth = '闰' + sNongliMonth
    
    nLunDay = int(nLunDay)
    # 生成农历日
    if nLunDay < 0 or nLunDay >= len(cDayName):
        raise ValueError('Error Month for LunDay')
    
    sNongliDay = cDayName[nLunDay]
    
    return sShuxiang, sTianGan, sDiZhi, sNongliMonth, sNongliDay


def GetLunarFeastIndex(nGreYear, nGreMonth, nGreDay):
    # 数组gLanarHoliDay存放每年的二十四节气对应的阳历日期
    # 每年的二十四节气对应的阳历日期几乎固定，平均分布于十二个月中
    # 1月 2月 3月 4月 5月 6月
    # 小寒 大寒 立春 雨水 惊蛰 春分 清明 谷雨 立夏 小满 芒种 夏至
    # 7月 8月 9月 10月 11月 12月
    # 小暑 大暑 立秋 处暑 白露 秋分 寒露 霜降 立冬 小雪 大雪 冬至
    #**********************************
    # 节气无任何确定规律,所以只好存表,要节省空间,所以....
    #**********************************}
    # 数据格式说明:
    # 如1901年的节气为
    # 1月 2月 3月 4月 5月 6月 7月 8月 9月 10月 11月 12月
    # 6, 21, 4, 19, 6, 21, 5, 21, 6,22, 6,22, 8, 23, 8, 24, 8, 24, 8, 24, 8, 23, 8, 22
    # 9, 6, 11,4, 9, 6, 10,6, 9,7, 9,7, 7, 8, 7, 9, 7, 9, 7, 9, 7, 8, 7, 15
    # 上面第一行数据为每月节气对应日期,15减去每月第一个节气,每月第二个节气减去15得第二行
    # 这样每月两个节气对应数据都小于16,每月用一个字节存放,高位存放第一个节气数据,低位存放
    # 第二个节气的数据,可得下表
    gLunarHolDay = settings.gLunarHolDay

    flag = gLunarHolDay[(nGreYear - 1901) * 12 + nGreMonth - 1]

    if nGreDay < 15:
        iday = 15 - ((flag >> 4) & 0x0f)
        n = 0
    else:
        iday = ((flag) & 0x0f) + 15
        n = 1

    if iday == nGreDay:
        return (nGreMonth - 1) * 2 + n + 1

    return 25


def Get24LunarFeast(xxx_todo_changeme3):
    (nGreYear, nGreMonth, nGreDay) = xxx_todo_changeme3
    HolText = settings.HolText

    holiIndex = GetLunarFeastIndex(nGreYear, nGreMonth, nGreDay)
    
    if holiIndex:
        sFeast = HolText[holiIndex - 1]
    else:
        sFeast = ''

    nFeastMonth = 0
    
    for n in range(1, 31):
        str_Hol = HolText[GetLunarFeastIndex(nGreYear, nGreMonth, n) - 1]
        
        if not str_Hol == '':
            if str_Hol == "立春":
                nFeastMonth = 13 if nGreDay >= n else 14
                break

                # if nGreDay >= n:
                #     nFeastMonth = 13  # 当天在立春后
                # else:
                #     nFeastMonth = 14  # 当天在立春前

            if str_Hol == "惊蛰":
                nFeastMonth = 2 if nGreDay >= n else 1
                break

                # if nGreDay >= n:
                #     nFeastMonth = 2  # 当天在惊蛰后
                # else:
                #     nFeastMonth = 1  # 当天在惊蛰前（下同）
                # break

            if str_Hol == "清明":
                nFeastMonth = 3 if nGreDay >= n else 2
                break

                # if nGreDay >= n:
                #     nFeastMonth = 3
                # else:
                #     nFeastMonth = 2
                # break

            if str_Hol == "立夏":
                nFeastMonth = 4 if nGreDay >= n else 3
                break

                # if nGreDay >= n:
                #     nFeastMonth = 4
                # else:
                #     nFeastMonth = 3
                # break

            if str_Hol == "芒种":
                nFeastMonth = 5 if nGreDay >= n else 4
                break

                # if nGreDay >= n:
                #     nFeastMonth = 5
                # else:
                #     nFeastMonth = 4
            
            if str_Hol == "小暑":
                nFeastMonth = 6 if nGreDay >= n else 5
                break

                # if nGreDay >= n:
                #     nFeastMonth = 6
                # else:
                #     nFeastMonth = 5
            
            if str_Hol == "立秋":
                nFeastMonth = 7 if nGreDay >= n else 6
                break

                # if nGreDay >= n:
                #     nFeastMonth = 7
                # else:
                #     nFeastMonth = 6
            
            if str_Hol == "白露":
                nFeastMonth = 8 if nGreDay >= n else 7
                break

                # if nGreDay >= n:
                #     nFeastMonth = 8
                # else:
                #     nFeastMonth = 7

            if str_Hol == "寒露":
                nFeastMonth = 9 if nGreDay >= n else 8
                break

                # if nGreDay >= n:
                #     nFeastMonth = 9
                # else:
                #     nFeastMonth = 8

            if str_Hol == "立冬":
                nFeastMonth = 10 if nGreDay >= n else 9
                break

                # if nGreDay >= n:
                #     nFeastMonth = 10
                # else:
                #     nFeastMonth = 9

            if str_Hol == "大雪":
                nFeastMonth = 11 if nGreDay >= n else 10
                break
                # if nGreDay >= n:
                #     nFeastMonth = 11
                # else:
                #     nFeastMonth = 10

            if str_Hol == "小寒":
                nFeastMonth = 12 if nGreDay >= n else 11
                break
                # if nGreDay >= n:
                #     nFeastMonth = 12
                # else:
                #     nFeastMonth = 11
                # break

    return sFeast, nFeastMonth


def Get8Zi(xxx_todo_changeme4):
    (nGreYear, nGreMonth, nGreDay, nHour, nMinute) = xxx_todo_changeme4
    (sShuxiang, sTianGan, sDiZhi, sNongliMonth, sNongliDay) = GetLunarString(Gregorian2Lunar((nGreYear, nGreMonth, nGreDay)))
    
    nTianGan = ((nGreYear - 4) % 60) % 10
    
    # 时辰
    nShiCheng = int(nHour / 2)
    
    if nHour % 2 == 1:  # [a<=x<b)半开半闭
        nShiCheng += 1
    
    if nShiCheng == 12:
        nShiCheng = 0
    
    # 分钟
    nFeng = int(nMinute / 10)
    
    if nHour % 2 == 0:
        nFeng += 6  # 1'分'含120分钟

    # 年干支
    str_Year = sTianGan + sDiZhi
    # 月干支
    cListMonth = settings.cListMonth

    # 天干名称
    cTianGan = settings.cTianGan
    # 地支名称
    cDizhi = settings.cDizhi

    (sFeast, nFeastMonth) = Get24LunarFeast((nGreYear, nGreMonth, nGreDay))
    nMonth = nFeastMonth  # 二十四节气定年月支

    if nGreMonth == 12:
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
    nGongYuanYear = nGreYear % 100  # 公元纪年的最后两位
    
    if nGongYuanYear == 0:
        nGongYuanYear = 100  # 百年逢百
    
    nA = (nGongYuanYear % 12) * 5
    nB = int(nGongYuanYear / 4)

    if not nGongYuanYear % 4 == 0:
        nB = nB + 1
    
    nYuanDanGanZHi = nA + nB
    # 2.查表 以cListMonth排列
    # 1901～2000年间以甲戌作1向后推某年C的值，既是该年元旦的干支﹙2001～2100年间以己未作1﹚
    nGongYuan = nGreYear
    
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

    if nGreMonth == 1:
        nGanRun = nGanRun - 1
        nZhiRun = nZhiRun - 1
    elif nGreMonth == 2:
        nZhiRun = nZhiRun + 6
    elif nGreMonth == 3:
        nGanRun = nGanRun - 2
        nZhiRun = nZhiRun + 10
    elif nGreMonth == 4:
        nGanRun = nGanRun - 1
        nZhiRun = nZhiRun + 5
    elif nGreMonth == 5:
        nGanRun = nGanRun - 1
        nZhiRun = nZhiRun - 1
    elif nGreMonth == 6:
        nZhiRun += 6
    elif nGreMonth == 8:
        nGanRun += 1
        nZhiRun += 7
    elif nGreMonth == 9:
        nGanRun += 2
        nZhiRun += 2
    elif nGreMonth == 10:
        nGanRun += 2
        nZhiRun += 8
    elif nGreMonth == 11:
        nGanRun += 3
        nZhiRun += 3
    elif nGreMonth == 12:
        nGanRun += 3
        nZhiRun += 9

    nRunYear = 0

    # 四年一闰,百年不闰,四百年再闰
    if (nGreYear %
        400 == 0) or (not nGreYear %
                      100 == 0) and (nGreYear %
                                     4 == 0):
        if nGreMonth > 2:
            nRunYear += 1

    cListTime = settings.cListTime
    # (nDayGan）+（nDay）+（所求月的天干加减数、闰年三月以后减1）÷10
    nTodayGan = (nDayGan + nGreDay + nGanRun + nRunYear) % 10
    #（所求年份的元旦地支）+（所求日期）+（所求月的地支加减数、闰年三月以后减1）÷12
    nTodayZhi = (nDayZhi + nGreDay + nZhiRun + nRunYear) % 12

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
    
    str_Minute = cListTime[nFeng][int(nTimeGan % 5)]

    # 四柱 + 考时 + 十字
    return str_Year, str_Month, str_Day, str_Time, str_Minute


if __name__ == '__main__':
    print (GetLunarString((2013, 5, 26, False)))
    print (Lunar2Gregorian((2013, 4, 10, True)))
    print (Gregorian2Lunar((2012, 1, 3)))
    print (Get24LunarFeast((2013, 5, 4)))
    print (Get8Zi((2012,5,4,0,0)))
