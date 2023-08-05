
import numpy as np
import pandas as pd

from .factor_types import FinQualityFactor
from .basic_factors import GrossProfitFactor, IncomeTTMFactor, NetProfitTTMFactor, AdjNetAssetAvgFactor, TotalAssetAvgFactor, FixAssetAvgFactor
from .utils import normalize


class GrossMarginFactor(FinQualityFactor):
    # 毛利率
    def __init__(self):
        super().__init__('gr_mar')

    def calc(self):
        # 过去四个季度的毛利润除以营业收入
        self._factor = GrossProfitFactor().get() / IncomeTTMFactor().get().replace({0: np.nan})


class ReturnOnAssetsFactor(FinQualityFactor):
    # 资产回报率
    def __init__(self):
        super().__init__('roa')

    def calc(self):
        # 过去四个季度的净利润除以总资产
        self._factor = NetProfitTTMFactor().get() / TotalAssetAvgFactor().get().replace({0: np.nan})


class ReturnOnEquityFactor(FinQualityFactor):
    # 股本回报率
    def __init__(self):
        super().__init__('roe')

    def calc(self):
        # 过去四个季度的净利润除以调整净资产
        self._factor = NetProfitTTMFactor().get() / AdjNetAssetAvgFactor().get().replace({0: np.nan})


class TurnoverRateOfFAFactor(FinQualityFactor):
    # 固定资产周转率
    def __init__(self):
        super().__init__('tr_fa')

    def calc(self):
        # 过去四个季度的营业收入除以固定资产
        self._factor = IncomeTTMFactor().get() / FixAssetAvgFactor().get().replace({0: np.nan})


class MixFinQualityFactor(FinQualityFactor):
    # 合成因子
    def __init__(self):
        super().__init__('mixf')
        self._universe: str = 'default'

    # TODO: 这个接口写的不好，暂时先这样
    def set_universe(self, universe: str):
        self._universe = universe



    def calc(self):
        index = GrossMarginFactor().get(self._universe).index
        columns = GrossMarginFactor().get(self._universe).columns
        self._factor = pd.DataFrame((normalize(GrossMarginFactor().get(self._universe).T) + normalize(ReturnOnAssetsFactor().get(self._universe).T) +
                                    normalize(ReturnOnEquityFactor().get(self._universe).T) + normalize(TurnoverRateOfFAFactor().get(self._universe).T)).T, index=index, columns=columns)
