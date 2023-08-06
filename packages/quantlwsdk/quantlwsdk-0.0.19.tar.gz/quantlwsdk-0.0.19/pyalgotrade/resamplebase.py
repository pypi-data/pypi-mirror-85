# PyAlgoTrade
#
# Copyright 2011-2018 Gabriel Martin Becedillas Ruiz
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import abc
import datetime

import six

from pyalgotrade.utils import dt
from pyalgotrade import bar
from pyalgotrade import observer

from pyalgotrade import config
from pyalgotrade import commonHelpBylw
from pyalgotrade import calendayBylw
import pandas as pd

@six.add_metaclass(abc.ABCMeta)
class TimeRange(object):

    @abc.abstractmethod
    def belongs(self, dateTime):
        raise NotImplementedError()

    @abc.abstractmethod
    def getBeginning(self):
        raise NotImplementedError()

    # 1 past the end
    @abc.abstractmethod
    def getEnding(self):
        raise NotImplementedError()


class IntraDayRange(TimeRange):
    def __init__(self, dateTime, frequency):
        super(IntraDayRange, self).__init__()
        assert isinstance(frequency, int)
        assert frequency > 1
        assert frequency < bar.Frequency.DAY

        ts = int(dt.datetime_to_timestamp(dateTime))
        slot = int(ts / frequency)
        slotTs = slot * frequency
        self.__begin = dt.timestamp_to_datetime(slotTs, not dt.datetime_is_naive(dateTime))
        if not dt.datetime_is_naive(dateTime):
            self.__begin = dt.localize(self.__begin, dateTime.tzinfo)
        self._end = self.__begin + datetime.timedelta(seconds=frequency)



    def belongs(self, dateTime):
        return dateTime >= self.__begin and dateTime < self._end

    def getBeginning(self):
        return self.__begin

    def getEnding(self):
        return self._end

    # lw李文添加了一个symbol参数，因为datetime 和frequency 还是无法 确定一个周期的结束时间，
    # 比如国内期货，你给定10：44 frequency为3min周期，你算出来的结束时间肯定是落在10:15和10：30之间，这不对。
class BarIntraDayRange(TimeRange):
    def __init__(self, dateTime, frequency,symbol,aNewTradeCalendar):
        # super(BarIntraDayRange, self).__init__(dateTime,frequency)

        assert isinstance(frequency, int)
        assert frequency > 1
        assert frequency < bar.Frequency.DAY

        #dateTime 是datetime 类型

        self.__begin,self._end=aNewTradeCalendar.getFreRangeByDt(symbol,dateTime,frequency)


    #     #获取合约的日线的开始时间
    #     ts = int(dt.datetime_to_timestamp(dateTime))
    #     slot = int(ts / frequency)
    #     slotTs = slot * frequency
    #     self.__begin = dt.timestamp_to_datetime(slotTs, not dt.datetime_is_naive(dateTime))
    #     if not dt.datetime_is_naive(dateTime):
    #         self.__begin = dt.localize(self.__begin, dateTime.tzinfo)
    #     self._end = self.__begin + datetime.timedelta(seconds=frequency)
    #
    #     self.aNewTradeCalendar=aNewTradeCalendar
    #
    #     #如果结束时间落在了10：15到10：30之间
    #     time15=datetime.time(hour=10, minute=15)
    #     time30=datetime.time(hour=10, minute=30)
    #     if self._end.time()< time30 and \
    #             self._end.time()> time15 and \
    #             commonHelpBylw.isChinaCommodiFutures(symbol):
    #
    #         dt15=datetime.datetime.combine(d.date(2020,1,1), time15)
    #         dt30 = datetime.datetime.combine(d.date(2020, 1, 1), time30)
    #         deltaTime=dt30-dt15
    #         self._end=self._end+deltaTime
    #         return
    #
    #     # 如果结束时间落在了11：30到13：30之间
    #     flag,delta=calendayBylw.isMiddleRestTime(self._end.time(), symbol)
    #     if flag:
    #         self._end = self._end + delta
    #         return
    #
    # #如果结束时间落在了晚上23：00到第二天09：00之间
    #     # 根据具体合约，调整结束时间
    #
    #
    #     dTime=calendayBylw.strTimeToDTime(dateList[0][1])
    #
    #     if self._end.time()> dTime and \
    #             commonHelpBylw.isChinaCommodiFutures(symbol):
    #
    #         if len(dateList)>1:
    #             detltatime = calendayBylw.getTimeDelta(dTime, calendayBylw.strTimeToDTime(dateList[1][0]))
    #             self._end=self._end+detltatime
    #
    #             #调整交易日
    #             #即如果是周六，则要调整到下一个交易日
    #
    #             strDate=self._end.strftime('%Y-%m-%d')
    #             if not self.aNewTradeCalendar.isTradingDate(strDate):
    #                 nextTtradeDate=self.aNewTradeCalendar.mDatesOffset(strDate,leftOrright=1)
    #                 d=datetime.datetime.strptime(nextTtradeDate,'%Y-%m-%d')
    #                 self._end=datetime.datetime.combine(d.date(), self._end.time())

            # return
    def getBeginning(self):
        return self.__begin

    def getEnding(self):
        return self._end
    def belongs(self, dateTime):
        print('barintradayRange:',dateTime,' ',self._end)
        return dateTime > self.__begin and dateTime <= self._end

    # def isTimeFilled(self):
    #     if dateTime <= self._end
    
class DayRange(TimeRange):
    def __init__(self, dateTime):
        super(DayRange, self).__init__()
        self.__begin = datetime.datetime(dateTime.year, dateTime.month, dateTime.day)
        if not dt.datetime_is_naive(dateTime):
            self.__begin = dt.localize(self.__begin, dateTime.tzinfo)
        self._end = self.__begin + datetime.timedelta(days=1)

    def belongs(self, dateTime):
        return dateTime >= self.__begin and dateTime < self._end

    def getBeginning(self):
        return self.__begin

    def getEnding(self):
        return self._end


class MonthRange(TimeRange):
    def __init__(self, dateTime):
        super(MonthRange, self).__init__()
        self.__begin = datetime.datetime(dateTime.year, dateTime.month, 1)

        # Calculate the ending date.
        if dateTime.month == 12:
            self._end = datetime.datetime(dateTime.year + 1, 1, 1)
        else:
            self._end = datetime.datetime(dateTime.year, dateTime.month + 1, 1)

        if not dt.datetime_is_naive(dateTime):
            self.__begin = dt.localize(self.__begin, dateTime.tzinfo)
            self._end = dt.localize(self._end, dateTime.tzinfo)

    def belongs(self, dateTime):
        return dateTime >= self.__begin and dateTime < self._end

    def getBeginning(self):
        return self.__begin

    def getEnding(self):
        return self._end


def is_valid_frequency(frequency):
    assert(isinstance(frequency, int))
    assert(frequency > 1)

    if frequency < bar.Frequency.DAY:
        ret = True
    elif frequency == bar.Frequency.DAY:
        ret = True
    elif frequency == bar.Frequency.MONTH:
        ret = True
    else:
        ret = False
    return ret

#lw李文添加了一个symbol参数，因为datetime 和frequency 还是无法 确定一个周期的结束时间，
#比如国内期货，你给定10：44 frequency为3min周期，你算出来的结束时间肯定是落在10:15和10：30之间，这不对。
def build_range(dateTime, frequency,symbol):
    assert(isinstance(frequency, int))
    assert(frequency > 1)

    if frequency < bar.Frequency.DAY:
        ret = IntraDayRange(dateTime, frequency,symbol)
    elif frequency == bar.Frequency.DAY:
        ret = DayRange(dateTime)
    elif frequency == bar.Frequency.MONTH:
        ret = MonthRange(dateTime)
    else:
        raise Exception("Unsupported frequency")
    return ret


@six.add_metaclass(abc.ABCMeta)
class Grouper(object):

    def __init__(self, timeRange,beginBarDt=False):

        if beginBarDt:

            self.__groupDateTime = timeRange.getBeginning()
        else:
            self.__groupDateTime = timeRange.getEnding()
        self._timeRange=timeRange

        self._groupFilledEvent = observer.Event() #事件，如果最后一个bar进程了，构成grouper的满了，那么立刻推送相应的函数。
    def getGroupFilledEvent(self):
        return self._groupFilledEvent
    def getDateTime(self):
        return self.__groupDateTime

    @abc.abstractmethod
    def addValue(self, value):
        """Add a value to the group."""
        raise NotImplementedError()

    @abc.abstractmethod
    def getGrouped(self):
        """Return the grouped value."""
        raise NotImplementedError()


    def belongs(self, dateTime_):
        return self._timeRange.belongs(dateTime_)

    def getEnding(self):
        return self._timeRange.getEnding()
        
    
