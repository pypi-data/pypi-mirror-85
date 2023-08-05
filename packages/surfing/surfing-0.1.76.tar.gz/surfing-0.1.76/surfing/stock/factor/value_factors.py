
import numpy as np
import pandas as pd

from .factor_types import ValueFactor
from .basic_factors import MarketValueFactor, AdjNetAssetAvgFactor, NetProfitTTMFactor, TotalRevenueTTMFactor
from .basic_factors import EBITDATTMFactor, EntValueFactor, DividendYearlyFactor
from .utils import normalize


class NAToMVFactor(ValueFactor):
    # 净市率
    def __init__(self):
        super().__init__('na_mv')

    def calc(self):
        # 净资产 / 总市值，即市净率倒数
        self._factor = AdjNetAssetAvgFactor().get() / MarketValueFactor().get().replace({0: np.nan})


class NPToMVFactor(ValueFactor):
    # 盈利收益比
    def __init__(self):
        super().__init__('np_mv')

    def calc(self):
        # 净利润 / 总市值，即市盈率倒数
        self._factor = NetProfitTTMFactor().get() / MarketValueFactor().get().replace({0: np.nan})


class SPSToPFactor(ValueFactor):
    # 营收股价比
    def __init__(self):
        super().__init__('sps_p')

    def calc(self):
        # 每股销售额 / 股价，即市销率倒数
        self._factor = TotalRevenueTTMFactor().get() / MarketValueFactor().get().replace({0: np.nan})


class DividendYieldFactor(ValueFactor):
    # 股息率
    def __init__(self):
        super().__init__('dys')

    def calc(self):
        # 过去12个月总派息额 / 总市值
        self._factor = DividendYearlyFactor().get() / MarketValueFactor().get().replace({0: np.nan})


class EBITDAToMVFactor(ValueFactor):
    # EBITDA股价比
    def __init__(self):
        super().__init__('eb_mv')

    def calc(self):
        # EBITDA（税息折旧及摊销前利润） / 总市值
        self._factor = EBITDATTMFactor().get() / MarketValueFactor().get().replace({0: np.nan})


class EBITDAToEVFactor(ValueFactor):
    # EBITDA企业价值比
    def __init__(self):
        super().__init__('eb_ev')

    def calc(self):
        # EBITDA（税息折旧及摊销前利润） / 企业价值, 即企业倍数的倒数
        self._factor = EBITDATTMFactor().get() / EntValueFactor().get().replace({0: np.nan})


class MixValueFactor(ValueFactor):
    # 合成因子
    def __init__(self):
        super().__init__('mixv')
        self._universe: str = 'default'

    # TODO: 这个接口写的不好，暂时先这样
    def set_universe(self, universe: str):
        self._universe = universe

    def calc(self):
        index = NAToMVFactor().get(self._universe).index
        columns = NAToMVFactor().get(self._universe).columns
        self._factor = pd.DataFrame((normalize(NAToMVFactor().get(self._universe).T) + normalize(NPToMVFactor().get(self._universe).T) + normalize(SPSToPFactor().get(self._universe).T) +
                                    normalize(DividendYieldFactor().get(self._universe).T) + normalize(EBITDAToMVFactor().get(self._universe).T) + normalize(EBITDAToEVFactor().get(self._universe).T)).T, index=index, columns=columns)
