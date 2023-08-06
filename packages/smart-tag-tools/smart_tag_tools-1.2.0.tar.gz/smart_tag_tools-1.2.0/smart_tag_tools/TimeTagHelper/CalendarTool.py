import sxtwl

ymc = [u"十一", u"十二", u"正", u"二", u"三", u"四", u"五", u"六", u"七", u"八", u"九", u"十"]
rmc = [u"初一", u"初二", u"初三", u"初四", u"初五", u"初六", u"初七", u"初八", u"初九", u"初十",
       u"十一", u"十二", u"十三", u"十四", u"十五", u"十六", u"十七", u"十八", u"十九",
       u"二十", u"廿一", u"廿二", u"廿三", u"廿四", u"廿五", u"廿六", u"廿七", u"廿八", u"廿九", u"三十", u"卅一"]

lunar = sxtwl.Lunar()  # 实例化日历库


class CalendarTool:
    """
    万年历工具
    """

    @staticmethod
    def __lunar_to_solar__(y, m, d):
        """
        # 阴历转阳历
        :param y:年
        :param m: 月
        :param d: 日
        :return:
        """
        day = lunar.getDayByLunar(y, m, d, False)
        return '{}年{}月{}日'.format(day.y, day.m, day.d)

    @staticmethod
    def __solar_to_lunar__(y, m, d):
        """
        阳历转阴历
        :param y:
        :param m:
        :param d:
        :return:
        """
        day = lunar.getDayBySolar(y, m, d)
        return '{}年{}月{}日'.format(y, ymc[day.Lmc], rmc[day.Ldi])
