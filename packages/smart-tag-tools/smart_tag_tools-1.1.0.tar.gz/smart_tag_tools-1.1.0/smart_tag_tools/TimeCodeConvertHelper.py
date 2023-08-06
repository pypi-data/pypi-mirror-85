import math


class TimeCodeConvertHelper(object):
    """
    时码转换帮助类
    """
    # endregion

    # region 25

    m_mpcStRate25 = 50  # PAL field frequency

    MpcStFrameRate25 = 25  # PAL frame  frequency

    MpcStScale25 = 1  # PAL scale

    # endregion

    # region 2997

    m_mpcStRate2997 = 60000  # NTSC field frequency

    MpcStFrameRate2997 = 30000  # NTSC frame  frequency

    MpcStScale2997 = 1001  # NTSC scale

    # endregion

    # region 30

    m_mpcStRate30 = 60  # 30-F field frequency

    MpcStFrameRate30 = 30  # 30-F frame frequency

    MpcStScale30 = 1  # 30-F scale

    # endregion

    # region 24

    m_mpcStRate24 = 48  # 24-F field frequency

    MpcStFrameRate24 = 24  # 24-F field frequency

    MpcStScale24 = 1  # 24-F scale

    # endregion

    # region 2398

    m_mpcStRate2398 = 48000  # 2398-F field frequency

    MpcStFrameRate2398 = 24000  # 2398-F frame frequency

    MpcStScale2398 = 1001  # 2398-F scale

    # endregion

    # region 50

    m_mpcStRate50 = 50  # PAL field frequency

    MpcStFrameRate50 = 50  # PAL frame  frequency

    MpcStScale50 = 1  # PAL scale

    # endregion

    # region 5994

    m_mpcStRate5994 = 60000  # NTSC field frequency

    MpcStFrameRate5994 = 60000  # NTSC frame  frequency

    MpcStScale5994 = 1001  # NTSC scale

    # endregion

    # region 60

    m_mpcStRate60 = 60  # 60-F field frequency

    MpcStFrameRate60 = 60  # 60-F frame frequency

    MpcStScale60 = 1  # 60-F scale

    # endregion

    # region 25 Frame

    MpcFramesSecond25 = 25  # 25 Frame: frames per second

    MpcFramesMinute25 = 1500  # 25 Frame: frames per minute

    MpcFramesHour25 = 90000  # 25 Frame: frames per hour

    # endregion

    # region 24 DROP Frame

    MpcFramesMinute24Drop = 1438  # 24 DROP Frame: frames per minute

    MpcFrames10Minutes24Drop = 14382  # 24 DROP Frame: frames per 10 minutes

    MpcFramesHour24Drop = 86292  # 24 DROP Frame: frames per hour

    MpcFramesSecond24 = 24  # 24 Frame: frames per second

    MpcFramesMinute24 = 1440  # 24 Frame: frames per minute

    MpcFramesHour24 = 86400  # 24 Frame: frames per hour

    MpcFramesSecondNodrop30 = 30  # 30 NO_DROP Frame: frames per second

    MpcFramesMinuteNodrop30 = 1800  # 30 NO_DROP Frame: frames per minute

    MpcFramesHourNodrop30 = 108000  # 30 NO_DROP Frame: frames per hour

    # endregion

    # region 30 DROP Frame

    MpcFramesMinute30Drop = 1798  # 30 DROP Frame: frames per minute

    MpcFrames10Minutes30Drop = 17982  # 30 DROP Frame: frames per 10 minutes

    MpcFramesHour30Drop = 107892  # 30 DROP Frame: frames per hour

    # endregion

    # region 50 Frame

    MpcFramesSecond50 = 50  # 25 Frame: frames per second

    MpcFramesMinute50 = 3000  # 25 Frame: frames per minute

    MpcFramesHour50 = 180000  # 25 Frame: frames per hour

    # endregion

    # region 60 DROP Frame

    MpcFramesMinute60Drop = 3596  # 60 DROP Frame: frames per minute

    MpcFrames10Minutes60Drop = 35964  # 60 DROP Frame: frames per 10 minutes

    MpcFramesHour60Drop = 215784  # 60 DROP Frame: frames per hour

    # endregion

    # region 60 Frame

    MpcFramesSecond60 = 60  # 60 Frame: frames per second

    MpcFramesMinute60 = 3600  # 60 Frame: frames per minute

    MpcFramesHour60 = 216000  # 60 Frame: frames per hour

    @staticmethod
    def __data_type_checker(args):
        """
        数据类型检查器
        :param args:
        :return:
        """
        for k, v in args:
            if not isinstance(k, v):
                if v == float and isinstance(k, int):
                    pass
                else:
                    raise TypeError('传入的参数类型错误')

    def Frame2L100NsByScale(self, lFrame, dRate, dScale):
        """
        帧转百纳秒
        :param lFrame: 帧
        :param dRate: 帧率
        :param dScale:
        :return:百纳秒
        """
        self.__data_type_checker(((lFrame, int), (dRate, float), (dScale, float)))
        dFrameRate = float(self.MpcStFrameRate25)
        dFrameScale = float(self.MpcStScale25)
        dFrameRate, dFrameScale = self.__Rate2ScaleFrameRateAndFrameScale(dRate, dScale, dFrameRate, dFrameScale)
        return int(math.floor(lFrame * pow(10, 7) * dFrameRate / dFrameScale))

    def Frame2L100Ns(self, dFrame, dFrameRate):
        """
        帧转百纳秒
        :param dFrame: 帧
        :param dFrameRate: 帧率
        :return:
        """
        self.__data_type_checker(((dFrame, int), (dFrameRate, float)))
        dRate = float(self.MpcStFrameRate25)
        dScale = float(self.MpcStScale25)
        dRate, dScale = self.__FrameRate2RateAndScale(dFrameRate, dRate, dScale)
        return int(math.floor(dFrame * dScale * pow(10, 7) / dRate))

    def __Rate2ScaleFrameRateAndFrameScale(self, dRate, dScale, dFrameRate, dFrameScale):
        """
        帧率修正
        :param dRate: 帧率
        :param dScale: 修正值
        :param dFrameRate:
        :param dFrameScale:
        :return:
        """
        self.__data_type_checker(((dRate, float), (dScale, float), (dFrameRate, float), (dFrameScale, float)))
        if ((dRate == self.MpcStFrameRate25 and dScale == self.MpcStScale25) or (
                dRate * self.MpcStScale25 == dScale * self.MpcStFrameRate25)):
            dFrameRate = self.MpcStFrameRate25
            dFrameScale = self.MpcStScale25
        elif ((dRate == self.MpcStFrameRate2997 and dScale == self.MpcStScale2997) or (
                dRate * self.MpcStScale2997 == dScale * self.MpcStFrameRate2997)):
            dFrameRate = self.MpcStFrameRate2997
            dFrameScale = self.MpcStScale2997
        elif ((dRate == self.MpcStFrameRate30 and dScale == self.MpcStScale30) or (
                dRate * self.MpcStScale30 == dScale * self.MpcStFrameRate30)):
            dFrameRate = self.MpcStFrameRate30
            dFrameScale = self.MpcStScale30
        elif ((dRate == self.MpcStFrameRate24 and dScale == self.MpcStScale24) or (
                dRate * self.MpcStScale24 == dScale * self.MpcStFrameRate24)):
            dFrameRate = self.MpcStFrameRate24
            dFrameScale = self.MpcStScale24
        elif ((dRate == self.MpcStFrameRate2398 and dScale == self.MpcStScale2398) or (
                dRate * self.MpcStScale2398 == dScale * self.MpcStFrameRate2398)):
            dFrameRate = self.MpcStFrameRate2398
            dFrameScale = self.MpcStScale2398
        elif ((dRate == self.MpcStFrameRate50 and dScale == self.MpcStScale50) or (
                dRate * self.MpcStScale50 == dScale * self.MpcStFrameRate50)):
            dFrameRate = self.MpcStFrameRate50
            dFrameScale = self.MpcStScale50
        elif ((dRate == self.MpcStFrameRate5994 and dScale == self.MpcStScale5994) or (
                dRate * self.MpcStScale5994 == dScale * self.MpcStFrameRate5994)):
            dFrameRate = self.MpcStFrameRate5994
            dFrameScale = self.MpcStScale5994
        elif ((dRate == self.MpcStFrameRate60 and dScale == self.MpcStScale60) or (
                dRate * self.MpcStScale60 == dScale * self.MpcStFrameRate60)):
            dFrameRate = self.MpcStFrameRate60
            dFrameScale = self.MpcStScale60
        return dFrameRate, dFrameScale

    def __FrameRate2RateAndScale(self, dFrameRate, dRate, dScale):
        """
        获取帧率和修正值
        :param dFrameRate:输入帧率
        :param dRate:
        :param dScale:
        :return:
        """
        self.__data_type_checker(((dFrameRate, float), (dRate, float), (dScale, float)))
        if (abs(dFrameRate - self.MpcStFrameRate25 / float
            (self.MpcStScale25)) < 0.01):
            dRate = self.MpcStFrameRate25
            dScale = self.MpcStScale25
        elif (abs(dFrameRate - self.MpcStFrameRate2997 / float
            (self.MpcStScale2997)) < 0.01):
            dRate = self.MpcStFrameRate2997
            dScale = self.MpcStScale2997
        elif (abs(dFrameRate - self.MpcStFrameRate30 / float
            (self.MpcStScale30)) < 0.01):
            dRate = self.MpcStFrameRate30
            dScale = self.MpcStScale30
        elif (abs(dFrameRate - self.MpcStFrameRate24 / float
            (self.MpcStScale24)) < 0.01):
            dRate = self.MpcStFrameRate24
            dScale = self.MpcStScale24
        elif (abs(dFrameRate - self.MpcStFrameRate2398 / float
            (self.MpcStScale2398)) < 0.01):
            dRate = self.MpcStFrameRate2398
            dScale = self.MpcStScale2398
        elif (abs(dFrameRate - self.MpcStFrameRate50 / float
            (self.MpcStScale50)) < 0.01):
            dRate = self.MpcStFrameRate50
            dScale = self.MpcStScale50
        elif (abs(dFrameRate - self.MpcStFrameRate5994 / float
            (self.MpcStScale5994)) < 0.01):
            dRate = self.MpcStFrameRate5994
            dScale = self.MpcStScale5994
        elif (abs(dFrameRate - self.MpcStFrameRate60 / float
            (self.MpcStScale60)) < 0.01):
            dRate = self.MpcStFrameRate60
            dScale = self.MpcStScale60
        return dRate, dScale

    def L100Ns2FrameByScale(self, l100Ns, dRate, dScale):
        """
        百纳秒转帧
        :param l100Ns: 百纳秒
        :param dRate: 帧率
        :param dScale: 修正值
        :return:
        """
        self.__data_type_checker(((l100Ns, int), (dRate, float), (dScale, float)))
        dFrameRate = float(self.MpcStFrameRate25)
        dFrameScale = float(self.MpcStScale25)
        dFrameRate, dFrameScale = self.__Rate2ScaleFrameRateAndFrameScale(dRate, dScale, dFrameRate, dFrameScale)
        return int(math.floor(l100Ns / math.pow(10, 7) * dFrameRate / dFrameScale + 0.5))

    def L100Ns2Frame(self, l100Ns, dFrameRate):
        """
        百纳秒转帧
        :param l100Ns: 百纳秒
        :param dFrameRate: 帧率
        :return:
        """
        self.__data_type_checker(((l100Ns, int), (dFrameRate, float)))
        dRate = float(self.MpcStFrameRate25)
        dScale = float(self.MpcStScale25)
        dRate, dScale = self.__FrameRate2RateAndScale(dFrameRate, dRate, dScale)
        return int(math.floor(l100Ns * dRate / dScale / math.pow(10, 7) + 0.5))

    def Frame2TcByScale(self, dFrame, dRate, dScale, dropFrame):
        """
        帧转时码
        :param dFrame: 帧
        :param dRate: 帧率
        :param dScale:
        :param dropFrame:
        :return: 时码字符串
        """
        self.__data_type_checker(((dFrame, float), (dRate, float), (dScale, float), (dropFrame, bool)))
        strTc = ''
        if ((dRate == self.MpcStFrameRate25 and dScale == self.MpcStScale25) or (
                dRate * self.MpcStScale25 == dScale * self.MpcStFrameRate25)):
            dHour = int((math.floor(dFrame / self.MpcFramesHour25)))
            dResidue = int((math.floor(dFrame % self.MpcFramesHour25)))
            dMin = int((math.floor(float(dResidue) / self.MpcFramesMinute25)))
            dResidue = dResidue % self.MpcFramesMinute25
            dSec = int(math.floor(float(dResidue) / self.MpcFramesSecond25))
            dFra = int(math.floor(float(dResidue) % self.MpcFramesSecond25))
            strTc = self.__FormatTimeCodeString(dHour, dMin, dSec, dFra, False)
        elif ((dRate == self.MpcStFrameRate2997 and dScale == self.MpcStScale2997) or (
                dRate * self.MpcStScale2997 == dScale * self.MpcStFrameRate2997)):
            if dropFrame:
                dHour = int(math.floor(dFrame / self.MpcFramesHour30Drop))
                dResidue = int(math.floor(dFrame % self.MpcFramesHour30Drop))
                dMin = int(math.floor(float(10) * (dResidue / self.MpcFrames10Minutes30Drop)))
                dResidue = dResidue % self.MpcFrames10Minutes30Drop
                if dResidue >= self.MpcFramesMinuteNodrop30:
                    dResidue -= self.MpcFramesMinuteNodrop30
                    dMin += 1 + dResidue / self.MpcFramesMinute30Drop
                    dResidue %= self.MpcFramesMinute30Drop
                    dResidue += 2
                dSec = int(math.floor(float(dResidue) / self.MpcFramesSecondNodrop30))
                dFra = int(math.floor(float(dResidue) % self.MpcFramesSecondNodrop30))
                strTc = self.__FormatTimeCodeString(dHour, dMin, dSec, dFra, True)
            else:
                dHour = int(math.floor(float(dFrame) / self.MpcFramesHourNodrop30))
                dResidue = int(math.floor(float(dFrame) % self.MpcFramesHourNodrop30))
                dMin = int(math.floor(float(dResidue) / self.MpcFramesMinuteNodrop30))
                dResidue = dResidue % self.MpcFramesMinuteNodrop30
                dSec = int(math.floor(float(dResidue) / self.MpcFramesSecondNodrop30))
                dFra = int(math.floor(float(dResidue) % self.MpcFramesSecondNodrop30))
                strTc = self.__FormatTimeCodeString(dHour, dMin, dSec, dFra, False)
        elif ((dRate == self.MpcStFrameRate30 and dScale == self.MpcStScale30) or (
                dRate * self.MpcStScale30 == dScale * self.MpcStFrameRate30)):
            dHour = int(math.floor(float(dFrame) / self.MpcFramesHourNodrop30))
            dResidue = int(math.floor(float(dFrame) % self.MpcFramesHourNodrop30))
            dMin = int(math.floor(float(dResidue) / self.MpcFramesMinuteNodrop30))
            dResidue = dResidue % self.MpcFramesMinuteNodrop30
            dSec = int(math.floor(float(dResidue) / self.MpcFramesSecondNodrop30))
            dFra = int(math.floor(float(dResidue) % self.MpcFramesSecondNodrop30))
            strTc = self.__FormatTimeCodeString(dHour, dMin, dSec, dFra, False)
        elif ((dRate == self.MpcStFrameRate24 and dScale == self.MpcStScale24) or (
                dRate * self.MpcStScale24 == dScale * self.MpcStFrameRate24)):
            dHour = int(math.floor(float(dFrame) / self.MpcFramesHour24))
            dResidue = int(math.floor(float(dFrame) % self.MpcFramesHour24))
            dMin = int(math.floor(float(dResidue) / self.MpcFramesMinute24))
            dResidue = dResidue % self.MpcFramesMinute24
            dSec = int(math.floor(float(dResidue) / self.MpcFramesSecond24))
            dFra = int(math.floor(float(dResidue) % self.MpcFramesSecond24))
            strTc = self.__FormatTimeCodeString(dHour, dMin, dSec, dFra, False)
        elif ((dRate == self.MpcStFrameRate2398 and dScale == self.MpcStScale2398) or (
                dRate * self.MpcStScale2398 == dScale * self.MpcStFrameRate2398)):
            if dropFrame:
                dHour = int(math.floor(dFrame / self.MpcFramesHour24Drop))
                dResidue = int(math.floor(dFrame % self.MpcFramesHour24Drop))
                dMin = int(math.floor(float(10) * (dResidue / self.MpcFrames10Minutes24Drop)))
                dResidue = dResidue % self.MpcFrames10Minutes24Drop
                if dResidue >= self.MpcFramesMinute24:
                    dResidue -= self.MpcFramesMinute24
                    dMin += 1 + dResidue / self.MpcFramesMinute24Drop
                    dResidue %= self.MpcFramesMinute24Drop
                    dResidue += 2
                dSec = int(math.floor(float(dResidue) / self.MpcFramesSecond24))
                dFra = int(math.floor(float(dResidue) % self.MpcFramesSecond24))
                strTc = self.__FormatTimeCodeString(dHour, dMin, dSec, dFra, True)
            else:
                dHour = int(math.floor(float(dFrame) / self.MpcFramesHour24))
                dResidue = int(math.floor(float(dFrame) % self.MpcFramesHour24))
                dMin = int(math.floor(float(dResidue) / self.MpcFramesMinute24))
                dResidue = dResidue % self.MpcFramesMinute24
                dSec = int(math.floor(float(dResidue) / self.MpcFramesSecond24))
                dFra = int(math.floor(float(dResidue) % self.MpcFramesSecond24))
                strTc = self.__FormatTimeCodeString(dHour, dMin, dSec, dFra, False)
        elif ((dRate == self.MpcStFrameRate50 and dScale == self.MpcStScale50) or (
                dRate * self.MpcStScale50 == dScale * self.MpcStFrameRate50)):
            dHour = int(math.floor(dFrame / self.MpcFramesHour50))
            dResidue = int(math.floor(dFrame % self.MpcFramesHour50))
            dMin = int(math.floor(float(dResidue) / self.MpcFramesMinute50))
            dResidue = dResidue % self.MpcFramesMinute50
            dSec = int(math.floor(float(dResidue) / self.MpcFramesSecond50))
            dFra = int(math.floor(float(dResidue) % self.MpcFramesSecond50))
            strTc = self.__FormatTimeCodeString(dHour, dMin, dSec, dFra, False)
        elif ((dRate == self.MpcStFrameRate5994 and dScale == self.MpcStScale5994) or (
                dRate * self.MpcStScale5994 == dScale * self.MpcStFrameRate5994)):
            if dropFrame:
                dHour = int(math.floor(dFrame / self.MpcFramesHour60Drop))
                dResidue = int(math.floor(dFrame % self.MpcFramesHour60Drop))
                dMin = int(math.floor(float(10) * (dResidue / self.MpcFrames10Minutes60Drop)))
                dResidue = dResidue % self.MpcFrames10Minutes60Drop
                if dResidue >= self.MpcFramesMinute60:
                    dResidue -= self.MpcFramesMinute60
                    dMin += 1 + dResidue / self.MpcFramesMinute60Drop
                    dResidue %= self.MpcFramesMinute60Drop
                    dResidue += 4
                dSec = int(math.floor(float(dResidue) / self.MpcFramesSecond60))
                dFra = int(math.floor(float(dResidue) % self.MpcFramesSecond60))
                strTc = self.__FormatTimeCodeString(dHour, dMin, dSec, dFra, True)
            else:
                dHour = int(math.floor(float(dFrame) / self.MpcFramesHour60))
                dResidue = int(math.floor(float(dFrame) % self.MpcFramesHour60))
                dMin = int(math.floor(float(dResidue) / self.MpcFramesMinute60))
                dResidue = dResidue % self.MpcFramesMinute60
                dSec = int(math.floor(float(dResidue) / self.MpcFramesSecond60))
                dFra = int(math.floor(float(dResidue) % self.MpcFramesSecond60))
                strTc = self.__FormatTimeCodeString(dHour, dMin, dSec, dFra, False)

        elif ((dRate == self.MpcStFrameRate60 and dScale == self.MpcStScale60) or (
                dRate * self.MpcStScale60 == dScale * self.MpcStFrameRate60)):
            dHour = int(math.floor(float(dFrame) / self.MpcFramesHour60))
            dResidue = int(math.floor(float(dFrame) % self.MpcFramesHour60))
            dMin = int(math.floor(float(dResidue) / self.MpcFramesMinute60))
            dResidue = dResidue % self.MpcFramesMinute60
            dSec = int(math.floor(float(dResidue) / self.MpcFramesSecond60))
            dFra = int(math.floor(float(dResidue) % self.MpcFramesSecond60))
            strTc = self.__FormatTimeCodeString(dHour, dMin, dSec, dFra, False)
        return strTc

    def Frame2Tc(self, dFrame, dFrameRate, dropFrame):
        """
        帧转时码
        :param dFrame: 帧
        :param dFrameRate:帧率
        :param dropFrame: 是否丢帧
        :return:
        """
        self.__data_type_checker(((dFrame, int), (dFrameRate, float), (dropFrame, bool)))
        dRate = self.MpcStFrameRate25
        dScale = self.MpcStScale25
        dRate, dScale = self.__FrameRate2RateAndScale(dFrameRate, dRate, dScale)
        strTc = self.Frame2TcByScale(dFrame, dRate, dScale, dropFrame)
        return strTc

    def __FormatTimeCodeString(self, hours, minutes, seconds, frames, dropFrame):
        """
        格式化时码字符串
        :param hours: 小时数
        :param minutes: 分指数
        :param seconds: 秒数
        :param frames: 帧数
        :param dropFrame: 是否是丢帧
        :return: 格式化后的时码字符串
        """
        self.__data_type_checker(((hours, int), (minutes, int), (seconds, int), (frames, int), (dropFrame, bool)))
        hours = hours - 24 if hours >= 24 else hours
        minutes = minutes - 60 if minutes >= 60 else minutes
        seconds = seconds - 60 if seconds >= 60 else seconds
        framesSeparator = "."
        if not dropFrame:
            framesSeparator = ":"
        hours = int(math.floor(hours % 24.0))
        return "{0:0>2d}:{1:0>2d}{4}{2:0>2d}:{3:0>2d}".format(hours, minutes, seconds, frames, framesSeparator)

    def TimeCode2Frame(self, sTimeCode, dFrameRate, dropFrame):
        """
        时间字符串转帧
        :param sTimeCode: 时码
        :param dFrameRate: 帧率
        :param dropFrame: 是否是丢帧
        :return:
        """
        self.__data_type_checker(((sTimeCode, str), (dFrameRate, float), (dropFrame, bool)))
        sTimeCode = self.__FormatTimeCodeStringByFrame(sTimeCode, dFrameRate, dropFrame)
        dRate = float(self.MpcStFrameRate25)
        dScale = float(self.MpcStScale25)
        dRate, dScale = self.__FrameRate2RateAndScale(dFrameRate, dRate, dScale)
        ftcFrames = self.TimeCode2FrameByScale(sTimeCode, dFrameRate, dRate, dScale, dropFrame)
        newTc = self.Frame2Tc(ftcFrames, dFrameRate, dropFrame)
        newTc = newTc.replace(".", ":")
        sTimeCode = sTimeCode.replace(".", ":")
        if newTc != sTimeCode:
            ftcFrames = self.__GetFrameByTimeCode(sTimeCode, ftcFrames, True, 1, dFrameRate, dropFrame)
        return ftcFrames

    def __FormatTimeCodeStringByFrame(self, timeCode, dFrameRate, dropFrame):
        """
        格式化时码字符串
        :param timeCode: 时间字符串
        :param dFrameRate: 帧率
        :param dropFrame: 是否是丢帧
        :return:
        """
        self.__data_type_checker(((timeCode, str), (dFrameRate, float), (dropFrame, bool)))
        if timeCode:
            if len(timeCode) == 11:
                c = list(timeCode)
                if c[8] == '.':
                    c[8] = ':'
                    c[5] = '.'
                timeCode = ''.join(c)
            hours = 0
            minutes = 0
            seconds = 0
            frames = 0
            ftcs = timeCode.split(':')
            hours = int(ftcs[0])
            if len(ftcs) >= 4:
                minutes = int(ftcs[1])
                seconds = int(ftcs[2])
                if int(ftcs[3]) >= dFrameRate:
                    showframeRate = float(math.ceil(dFrameRate) - 1)
                    ftcs[3] = str(showframeRate)
                else:
                    if dropFrame:
                        dropM = ["00", "10", "20", "30", "40", "50"]
                        drop5994F = ["00", "01", "02", "03"]
                        dropF = ["00", "01"]
                        if ftcs[2] == "00" and ftcs[1] not in dropM and ftcs[3] in drop5994F:
                            if abs(60.0 - dFrameRate) < 0.1:
                                ftcs[3] = "04"
                            elif abs(30.0 - dFrameRate) < 0.1 or abs(24.0 - dFrameRate) < 0.1:
                                if ftcs[3] in dropF:
                                    ftcs[3] = "02"
                frames = int(ftcs[3])
            else:
                ftcssf = ftcs[1].split('.')
                minutes = int(ftcssf[0])
                seconds = int(ftcssf[1])
                if int(ftcs[2]) >= dFrameRate:
                    # region 修正最后一位 29.97最大显示29 25最大显示24
                    showframeRate = float(math.ceil(dFrameRate) - 1)
                    ftcs[2] = str(showframeRate)
                else:
                    # region 验证是否是丢帧时码
                    if dropFrame:
                        dropM = ["00", "10", "20", "30", "40", "50"]
                        drop5994F = ["00", "01", "02", "03"]
                        dropF = ["00", "01"]
                        if ftcssf[1] == "00" and dropM not in ftcssf[0] and ftcs[2] in drop5994F:
                            if abs(60.0 - dFrameRate) < 0.1:
                                ftcs[2] = "04"
                            elif abs(30.0 - dFrameRate) < 0.1 or abs(24.0 - dFrameRate) < 0.1:
                                if ftcs[2] in dropF:
                                    ftcs[2] = "02"
                frames = int(ftcs[2])
            return self.__FormatTimeCodeString(hours, minutes, seconds, frames, dropFrame)
        return "--:--:--:--"

    def TimeCode2FrameByScale(self, sTimeCode, frameRate, dRate, dScale, dropframe):
        """
        时间字符串转帧
        :param sTimeCode:时码
        :param frameRate:帧率
        :param dRate:
        :param dScale:
        :param dropframe:是否是丢帧
        :return:帧
        """
        self.__data_type_checker(
            ((sTimeCode, str), (frameRate, float), (dRate, float), (dScale, float), (dropframe, bool)))
        ftcFrames = 0
        if ((dRate == self.MpcStFrameRate25 and dScale == self.MpcStScale25) or (
                dRate * self.MpcStScale25 == dScale * self.MpcStFrameRate25)):
            ftcFrames = self.TimeCode2NdfFrame(sTimeCode, frameRate)
        elif ((dRate == self.MpcStFrameRate2997 and dScale == self.MpcStScale2997) or (
                dRate * self.MpcStScale2997 == dScale * self.MpcStFrameRate2997)):
            lHour = 0
            lMinute = 0
            lSecond = 0
            lFrame = 0
            lHour, lMinute, lSecond, lFrame = self.__TimeCode2Format(sTimeCode, lHour, lMinute, lSecond, lFrame,
                                                                     frameRate)
            if dropframe:
                ftcFrames += lHour * self.MpcFramesHour30Drop
                lwReste = int(lMinute / 10)
                ftcFrames += lwReste * self.MpcFrames10Minutes30Drop
                lwReste = lMinute % 10
                if lwReste > 0:
                    ftcFrames += self.MpcFramesMinuteNodrop30
                    ftcFrames += (lwReste - 1) * self.MpcFramesMinute30Drop
                    ftcFrames -= 2
                ftcFrames += lSecond * self.MpcFramesSecondNodrop30
                ftcFrames += lFrame
            else:
                ftcFrames = self.TimeCode2NdfFrame(sTimeCode, 30)
        elif ((dRate == self.MpcStFrameRate30 and dScale == self.MpcStScale30) or (
                dRate * self.MpcStScale30 == dScale * self.MpcStFrameRate30)):
            ftcFrames = self.TimeCode2NdfFrame(sTimeCode, frameRate)
        elif ((dRate == self.MpcStFrameRate24 and dScale == self.MpcStScale24) or (
                dRate * self.MpcStScale24 == dScale * self.MpcStFrameRate24)):
            ftcFrames = self.TimeCode2NdfFrame(sTimeCode, frameRate)
        elif ((dRate == self.MpcStFrameRate2398 and dScale == self.MpcStScale2398) or (
                dRate * self.MpcStScale2398 == dScale * self.MpcStFrameRate2398)):
            lHour = 0
            lMinute = 0
            lSecond = 0
            lFrame = 0
            lHour, lMinute, lSecond, lFrame = self.__TimeCode2Format(sTimeCode, lHour, lMinute, lSecond, lFrame,
                                                                     frameRate)
            if dropframe:
                ftcFrames += lHour * self.MpcFramesHour24
                lwReste = int(lMinute / 10)
                ftcFrames += lwReste * self.MpcFrames10Minutes24Drop
                lwReste = lMinute % 10
                if lwReste > 0:
                    ftcFrames += self.MpcFramesMinute60
                    ftcFrames += (lwReste - 1) * self.MpcFramesMinute24
                    ftcFrames -= 2
                ftcFrames += lSecond * self.MpcFramesSecond24
                ftcFrames += lFrame
            else:
                ftcFrames = self.TimeCode2NdfFrame(sTimeCode, 24)
        elif ((dRate == self.MpcStFrameRate50 and dScale == self.MpcStScale50) or (
                dRate * self.MpcStScale50 == dScale * self.MpcStFrameRate50)):
            ftcFrames = self.TimeCode2NdfFrame(sTimeCode, frameRate)
        elif ((dRate == self.MpcStFrameRate5994 and dScale == self.MpcStScale5994) or (
                dRate * self.MpcStScale5994 == dScale * self.MpcStFrameRate5994)):
            lHour = 0
            lMinute = 0
            lSecond = 0
            lFrame = 0
            lHour, lMinute, lSecond, lFrame = self.__TimeCode2Format(sTimeCode, lHour, lMinute, lSecond, lFrame,
                                                                     frameRate)
            if dropframe:
                ftcFrames += lHour * self.MpcFramesHour60Drop
                lwReste = int(lMinute / 10)
                ftcFrames += lwReste * self.MpcFrames10Minutes60Drop
                lwReste = lMinute % 10
                if lwReste > 0:
                    ftcFrames += self.MpcFramesMinute60
                    ftcFrames += (lwReste - 1) * self.MpcFramesMinute60Drop
                    ftcFrames -= 4
                ftcFrames += lSecond * self.MpcFramesSecond60
                ftcFrames += lFrame
            else:
                ftcFrames = self.TimeCode2NdfFrame(sTimeCode, 60)
        elif ((dRate == self.MpcStFrameRate60 and dScale == self.MpcStScale60) or (
                dRate * self.MpcStScale60 == dScale * self.MpcStFrameRate60)):
            ftcFrames = self.TimeCode2NdfFrame(sTimeCode, frameRate)
        return ftcFrames

    def __GetFrameByTimeCode(self, sTimeCode, ftcFrames, isAdded, corrValue, dFrameRate, dropFrame):
        """
        递归解决时码丢帧的问题
        :param sTimeCode:
        :param ftcFrames:
        :param isAdded:是否加修正值
        :param corrValue:修正值
        :param dFrameRate:
        :param dropFrame:
        :return:
        """
        self.__data_type_checker(
            ((sTimeCode, str), (ftcFrames, int), (isAdded, bool), (corrValue, int), (dFrameRate, float),
             (dropFrame, bool)))
        ftcNewFrames = 0
        if isAdded:
            ftcNewFrames = ftcFrames + corrValue
        else:
            ftcNewFrames = ftcFrames - corrValue
            corrValue += 1
        newTc = self.Frame2Tc(ftcNewFrames, dFrameRate, dropFrame)
        newTc = newTc.replace(".", ":")
        sTimeCode = sTimeCode.replace(".", ":")
        if newTc != sTimeCode:
            return self.__GetFrameByTimeCode(sTimeCode, ftcFrames, not isAdded, corrValue, dFrameRate, dropFrame)
        return ftcNewFrames

    def __TimeCode2Format(self, sTimeCode, lHour, lMinute, lSecond, lFrame, dFrameRate):
        """
        时间字符串格式化
        :param sTimeCode:
        :param lHour:
        :param lMinute:
        :param lSecond:
        :param lFrame:
        :param dFrameRate:
        :return: 帧数
        """
        self.__data_type_checker(
            ((sTimeCode, str), (lHour, int), (lMinute, int), (lSecond, int), (lFrame, int), (dFrameRate, float)))
        ftcCodes = sTimeCode.split(':')
        if len(ftcCodes) >= 4:
            lHour = int(ftcCodes[0])
            lMinute = int(ftcCodes[1])
            lSecond = int(ftcCodes[2])
            lFrame = int(ftcCodes[3])
        else:
            ftcssf = ftcCodes[1].split('.')
            lHour = int(ftcCodes[0])
            lMinute = int(ftcssf[0])
            lSecond = int(ftcssf[1])
            lFrame = int(ftcCodes[2])
        lHour = lHour - 24 if lHour >= 24 else lHour
        lMinute = lMinute - 60 if lMinute >= 60 else lMinute
        lSecond = lSecond - 60 if lSecond >= 60 else lSecond
        lFrame = lFrame - int(math.ceil(dFrameRate)) if lFrame >= math.ceil(dFrameRate) else lFrame
        return lHour, lMinute, lSecond, lFrame

    def TimeCode2NdfFrame(self, sTimeCode, dFrameRate):
        """
        时间字符串转秒(未考虑丢帧的情况)
        :param sTimeCode:
        :param dFrameRate:
        :return:帧数
        """
        self.__data_type_checker(((sTimeCode, str), (dFrameRate, float)))
        ftcSeconds = 0
        ftcFrames = 0
        lHour = 0
        lMinute = 0
        lSecond = 0
        lFrame = 0
        lHour, lMinute, lSecond, lFrame = self.__TimeCode2Format(sTimeCode, lHour, lMinute, lSecond, lFrame, dFrameRate)
        ftcSeconds += lHour * 60 * 60
        ftcSeconds += lMinute * 60
        ftcSeconds += lSecond
        ftcFrames += lFrame
        ftcFrames += self.Second2Frame(ftcSeconds, dFrameRate)
        return ftcFrames

    def Second2Frame(self, dbSec, dFrameRate):
        """
        秒转帧
        :param dbSec:秒数
        :param dFrameRate:帧率
        :return:帧数
        """
        self.__data_type_checker(((dbSec, float), (dFrameRate, float)))
        if dbSec >= 24 * 60 * 60:
            dbSec = dbSec - 24 * 60 * 60
            return self.Second2Frame(dbSec, dFrameRate)
        dbSec = math.ceil(dbSec * math.pow(10, 7))
        dRate = float(self.MpcStFrameRate25)
        dScale = float(self.MpcStScale25)
        dRate, dScale = self.__FrameRate2RateAndScale(dFrameRate, dRate, dScale)
        return int(math.floor(dbSec * dRate / dScale / math.pow(10, 7)))

    def L100Ns2Tc(self, l100Ns, dropFrame):
        """
        百纳秒转时码
        :param l100Ns: 百纳秒
        :param dropFrame: 是否是丢帧
        :return: 时码字符串
        """
        self.__data_type_checker(((l100Ns, int), (dropFrame, bool)))
        dHour = int(math.floor(l100Ns / (60 * 60 * math.pow(10, 7))))
        llResidue = int(l100Ns % (60 * 60 * math.pow(10, 7)))
        dMin = int(math.floor(llResidue / (60 * math.pow(10, 7))))
        llResidue = llResidue % int(math.floor(60 * math.pow(10, 7)))
        dSec = int(math.floor(llResidue / (math.pow(10, 7))))
        llResidue = llResidue % int(math.pow(10, 7))
        dFraction = int(math.floor(float(llResidue) / (10 * 1000 * 10)))
        return self.__FormatTimeCodeString(dHour, dMin, dSec, dFraction, dropFrame)

    def L100Ns2TcByFrame(self, l100Ns, dFrameRate, dropFrame):
        """
        百纳秒转时码
        :param l100Ns: 百纳秒
        :param dFrameRate: 帧率
        :param dropFrame:
        :return: 时码字符串
        """
        self.__data_type_checker(((l100Ns, int), (dFrameRate, float), (dropFrame, bool)))
        return self.Frame2Tc(self.L100Ns2Frame(l100Ns, dFrameRate), dFrameRate, dropFrame)