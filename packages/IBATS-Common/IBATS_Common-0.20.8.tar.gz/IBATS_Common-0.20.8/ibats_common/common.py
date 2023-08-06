#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author  : MG
@Time    : 2018/6/20 15:15
@File    : common.py
@contact : mmmaaaggg@163.com
@desc    : 
"""
from enum import IntEnum, unique, Enum


@unique
class PeriodType(IntEnum):
    """
    周期类型
    """
    Tick = 0
    Min1 = 1
    Min5 = 2
    Min10 = 3
    Min15 = 4
    Min30 = 5
    Hour1 = 10
    Day1 = 20
    Week1 = 30
    Mon1 = 40
    Year1 = 100

    @staticmethod
    def get_min_count(period_type) -> int:
        """
        返回给的周期类型对应的分钟数
        :param period_type:
        :return:
        """
        if PeriodType.Min1 == period_type:
            min_count = 1
        elif PeriodType.Min5 == period_type:
            min_count = 5
        elif PeriodType.Min10 == period_type:
            min_count = 10
        elif PeriodType.Min15 == period_type:
            min_count = 15
        elif PeriodType.Min30 == period_type:
            min_count = 30
        else:
            raise ValueError('不支持 %s 周期' % period_type)
        return min_count


@unique
class RunMode(IntEnum):
    """
    运行模式，目前支持两种：实时行情模式，回测模式
    """
    Realtime = 0
    Backtest = 1
    Backtest_FixPercent = 2


@unique
class CalcMode(IntEnum):
    """
    收益及账户计算模式
    """
    Normal = 0
    Margin = 1


@unique
class ExchangeName(IntEnum):
    """
    交易所名称
    """
    Default = 0
    HuoBi = 1
    BitMex = 2
    DataIntegration = 3
    LocalFile = 4           # Local test use only


@unique
class Direction(IntEnum):
    """买卖方向"""
    Short = -1  # 空头
    Long = 1  # 多头


@unique
class Action(IntEnum):
    """开仓平仓"""
    Open = 0  # 开仓
    Close = 1  # 平仓
    ForceClose = 2  # 强平
    CloseToday = 3  # 平今
    CloseYesterday = 4  # 平昨
    ForceOff = 5  # 强减
    LocalForceClose = 6  # 本地强平

    @staticmethod
    def create_by_offsetflag(offset_flag):
        """
        将 Api 中 OffsetFlag 变为 Action 类型
        :param offset_flag:
        :return:
        """
        if offset_flag == '0':
            return Action.Open
        elif offset_flag in {'1', '5'}:
            return Action.Close
        elif offset_flag == '3':
            return Action.CloseToday
        elif offset_flag == '4':
            return Action.CloseYesterday
        elif offset_flag == '2':
            return Action.ForceClose
        elif offset_flag == '6':
            return Action.LocalForceClose
        else:
            raise ValueError('Action不支持 %s' % offset_flag)


@unique
class PositionDateType(IntEnum):
    """今日持仓历史持仓标示"""
    Today = 1  # 今日持仓
    History = 2  # 历史持仓


@unique
class BacktestTradeMode(IntEnum):
    """
    回测模式下的成交模式
    """
    Order_2_Deal = 0    # 一种简单回测模式，无论开仓平仓等操作，下单即成交
    MD_2_Deal = 1       # 根据下单后行情变化确定何时成交
    NextOpen = 2        # 下一个行情数据的开盘价作为成交价格，相当于市价成交


@unique
class ContextKey(IntEnum):
    """
    策略执行逻辑中 context[key] 的部分定制化key
    """
    instrument_id_list = 0
    md_agent_key = 1
    period = 2


