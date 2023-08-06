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

import six

from pyalgotrade import dataseries
from pyalgotrade.dataseries import bards
from pyalgotrade import bar
from pyalgotrade import resamplebase
from apscheduler.schedulers.background import BackgroundScheduler
import  datetime

from threading import Lock



class AggFunGrouper(resamplebase.Grouper):
    def __init__(self, groupDateTime, value, aggfun):
        super(AggFunGrouper, self).__init__(groupDateTime)
        self.__values = [value]
        self.__aggfun = aggfun

    def addValue(self, value):
        self.__values.append(value)

    def getGrouped(self):
        return self.__aggfun(self.__values)


class BarGrouper(resamplebase.Grouper):
    def __init__(self, timeRange,bar_, frequency,beginBarDt=False):
        super(BarGrouper, self).__init__(timeRange,beginBarDt)
        self.__open = bar_.getOpen()
        self.__high = bar_.getHigh()
        self.__low = bar_.getLow()
        self.__close = bar_.getClose()
        self.__volume = bar_.getVolume()
        self.__adjClose = bar_.getAdjClose()
        self.__useAdjValue = bar_.getUseAdjValue()
        self.__frequency = frequency

    def addValue(self, value):
        self.__high = max(self.__high, value.getHigh())
        self.__low = min(self.__low, value.getLow())
        self.__close = value.getClose()
        self.__adjClose = value.getAdjClose()
        self.__volume += value.getVolume()

        if value.getDateTime()==self._timeRange.getEnding():
            self._groupFilledEvent.emit()

    def getGrouped(self):
        """Return the grouped value."""
        ret = bar.BasicBar(
            self.getDateTime(),
            self.__open, self.__high, self.__low, self.__close, self.__volume, self.__adjClose,
            self.__frequency
        )
        ret.setUseAdjustedValue(self.__useAdjValue)
        return ret


@six.add_metaclass(abc.ABCMeta)
class DSResampler(object):

    def initDSResampler(self, dataSeries, frequency):
        if not resamplebase.is_valid_frequency(frequency):
            raise Exception("Unsupported frequency")

        self.__frequency = frequency
        self.__grouper = None
        self.__range = None

        self.sched=None

        self._hamode= 'backtest_fast'  #标记行情是实时行情还是回测行情。


        # if hqmode in ['backtest_func', 'backtest_fast']:
        #     dataSeries.getNewValueEvent().subscribe(self.__onNewValue)
        # if hqmode in ['real', 'simulate']:
        #     self.sched = BackgroundScheduler()
        #     self.sched.start()
        #     dataSeries.getNewValueEvent().subscribe(self._onNewLiveModeValue)

        dataSeries.getNewValueEvent().subscribe(self.__onNewValue)

        self.lock_ = Lock()

    @abc.abstractmethod
    def buildGrouper(self, range_, value, frequency):
        raise NotImplementedError()

    # @abc.abstractmethod
    # def build_range(self, dateTime,frequency):
    #     raise NotImplementedError()

    def _gouperFillFun(self):
        self.appendWithDateTime(self.__grouper.getDateTime(), self.__grouper.getGrouped())
        self.__grouper=None
        # print(self.sched)
        if self.sched is not None:
            # print('rmove all jobs')
            self.sched.remove_all_jobs()

    def __onNewValue(self, dataSeries, dateTime, value):

        # print(dateTime)

        if self._hamode in ['backtest_func', 'backtest_fast']:
            if self.__grouper is None:
                self.__grouper = self.buildGrouper(dateTime, value, self.__frequency)
                self.__grouper.getGroupFilledEvent().subscribe(self._gouperFillFun)
            elif self.__grouper.belongs(dateTime):
                self.__grouper.addValue(value)
            else:

                #这种应该是那种 gouper成立后，但是有些bar错过了，或者没有行情，直接来了一个超越了gouper范围的bar。
                self.appendWithDateTime(self.__grouper.getDateTime(), self.__grouper.getGrouped())
                # self.__range = self.build_range(dateTime, self.__frequency)
                self.__grouper = self.buildGrouper(dateTime, value, self.__frequency)
                self.__grouper.getGroupFilledEvent().subscribe(self._gouperFillFun)
        if self._hamode in ['real', 'simulate']:

            self._onNewLiveModeValue(dataSeries, dateTime, value)

    def _onNewLiveModeValue(self, dataSeries, dateTime, value):

        # print('onlivehq')
        # print(dateTime,' ',value)
        if self.__grouper is None:
            self.__grouper = self.buildGrouper(dateTime, value, self.__frequency)
            if self.__grouper is None:#即如果调用buildGrouper的结果是 none，说明到达日内结束事件了，直接返回。
                return 
            self.__grouper.getGroupFilledEvent().subscribe(self._gouperFillFun)

            #准备定时器
            self.sched.add_job(self.pushLast, 'date', run_date=self.__grouper.getEnding()+datetime.timedelta(seconds=10),misfire_grace_time=60)



        else:

            self.lock_.acquire()
            if self.__grouper.belongs(dateTime):

                self.__grouper.addValue(value)
            self.lock_.release()
        # else:
        #     self.appendWithDateTime(self.__grouper.getDateTime(), self.__grouper.getGrouped())
        #     self.__range = self.build_range(dateTime, self.__frequency)
        #     if self.__range is not None:
        #         self.__grouper = self.buildGrouper(self.__range, value, self.__frequency)
        #
        #
        #     self.__grouper = None
        #     self.__range = None
        #     i=1

    def setHqmode(self,hqmode):


        #如果是实时模式，之前补充数据的，得先将原始的range清空，否则逻辑很混乱。当然这中间会丢失一个bar的数据，但是如果不是交易时间启动，是不会有 影响的。
        if self._hamode in ['backtest_func', 'backtest_fast'] and hqmode in ['real', 'simulate']:
            self.__range=None
            self.__grouper=None
        self._hamode=hqmode
        if self._hamode in ['real', 'simulate']:
            self.sched = BackgroundScheduler()
            self.sched.start()

    def pushLast(self):
        import datetime
        print('time sched: ',datetime.datetime.now())
        self.lock_.acquire()

        if self.__grouper is not None:
            self.appendWithDateTime(self.__grouper.getDateTime(), self.__grouper.getGrouped())
            self.__grouper = None
            self.__range = None

        self.lock_.release()

    def checkNow(self, dateTime):
        if self.__range is not None and not self.__range.belongs(dateTime):
            self.appendWithDateTime(self.__grouper.getDateTime(), self.__grouper.getGrouped())
            self.__grouper = None
            self.__range = None


class ResampledBarDataSeries(bards.BarDataSeries, DSResampler):
    """A BarDataSeries that will build on top of another, higher frequency, BarDataSeries.
    Resampling will take place as new values get pushed into the dataseries being resampled.

    :param dataSeries: The DataSeries instance being resampled.
    :type dataSeries: :class:`pyalgotrade.dataseries.bards.BarDataSeries`
    :param frequency: The grouping frequency in seconds. Must be > 0.
    :param maxLen: The maximum number of values to hold.
        Once a bounded length is full, when new items are added, a corresponding number of items are discarded
        from the opposite end.
    :type maxLen: int.

    .. note::
        * Supported resampling frequencies are:
            * Less than bar.Frequency.DAY
            * bar.Frequency.DAY
            * bar.Frequency.MONTH
    """

    def __init__(self, dataSeries, frequency, symbol,aNewTradeCalendar,beginBarDt=True,maxLen=None):
        if not isinstance(dataSeries, bards.BarDataSeries):
            raise Exception("dataSeries must be a dataseries.bards.BarDataSeries instance")

        super(ResampledBarDataSeries, self).__init__(maxLen)
        self.initDSResampler(dataSeries, frequency)

        self.symbol=symbol
        self.aNewTradeCalendar=aNewTradeCalendar
        self.beginBarDt=beginBarDt  #表示记录bar的时间的时候 ，用周期的开始时间，还是结束时间



    def checkNow(self, dateTime):
        """Forces a resample check. Depending on the resample frequency, and the current datetime, a new
        value may be generated.

       :param dateTime: The current datetime.
       :type dateTime: :class:`datetime.datetime`
        """

        return super(ResampledBarDataSeries, self).checkNow(dateTime)

    def buildGrouper(self, dateTime, value, frequency):
        #先构造range
        range_ = resamplebase.BarIntraDayRange(dateTime, frequency, self.symbol, self.aNewTradeCalendar)
        if range_.getEnding() is None:
            range_ = None
            return None

        agroupper=BarGrouper(range_,value, frequency,beginBarDt=self.beginBarDt)



        return agroupper

    # def build_range(self, dateTime, frequency):
    #
    #     range_=resamplebase.BarIntraDayRange(dateTime, frequency, self.symbol,self.aNewTradeCalendar)
    #     if range_.getEnding() is None:
    #         range_=None
    #     return range_


class ResampledDataSeries(dataseries.SequenceDataSeries, DSResampler):
    def __init__(self, dataSeries, frequency, aggfun, maxLen=None):
        super(ResampledDataSeries, self).__init__(maxLen)
        self.initDSResampler(dataSeries, frequency)
        self.__aggfun = aggfun

    def buildGrouper(self, range_, value, frequency):

        return AggFunGrouper(range_.getBeginning(), value, self.__aggfun)

