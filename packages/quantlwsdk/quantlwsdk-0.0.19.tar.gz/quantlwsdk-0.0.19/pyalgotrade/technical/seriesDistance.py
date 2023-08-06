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

"""
.. moduleauthor:: Gabriel Martin Becedillas Ruiz <gabriel.becedillas@gmail.com>
"""

from pyalgotrade import dataseries

#主要是2个序列相减。前项减去后项 再除以后后项



class seriesDistanceRatio(dataseries.SequenceDataSeries):
    """
    这个地方，为什么入参要是2个序列，因为这里是要判断任意两个序列的交叉。如果在
    类里面来生产序列，你不知道未来 是什么序列进来。一般可能是close的 ma 两个序列来判断交叉

    但是有时候，可能需要判断2个ema序列交叉。那在类里面写死就不好。
    """

    def __init__(self, dataSeries1, dataSeries2, maxLen=None):
        super(seriesDistanceRatio, self).__init__(maxLen)
        self._ds1=dataSeries1
        self._ds2=dataSeries2
        dataSeries2.getNewValueEvent().subscribe(self.__onNewValue)


    def __onNewValue(self, dataSeries, dateTime, value):

        #要计算当前时间的上穿还是下穿，至少得2个序列（包含当前序列在内）
        print(dateTime + ' seriesDistanceRatio on value')

        if len(self._ds1)>=1 and len(self._ds2)>=1:


            #首先检查时间
            dtFromDs1 = self._ds1.getDateTimes()[-1]
            dtFromDs2 = self._ds2.getDateTimes()[-1]
            assert (dtFromDs1 == dtFromDs2)



            newValue = 0
            #金叉

            if self._ds1[-1] is not None and self._ds2[-1] is not None:

                newValue=(self._ds1[-1]-self._ds2[-1])/self._ds2[-1]

                self.appendWithDateTime(dtFromDs1, newValue)

