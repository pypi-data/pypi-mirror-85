
import numpy as np

from .factor_types import TechFactor
from .basic_factors import StockPostPriceFactor
from .utils import get_day


class ReverseFactor(TechFactor):
    # 逆转
    def __init__(self):
        super().__init__('rev')

    def calc(self):
        spp = StockPostPriceFactor().get()
        ls = spp.index  # trading_day_list
        fac = spp.copy()
        for i in range(0, len(spp)):
            try:
                temp = get_day(30, ls, spp.index[i])
                fac.iloc[i] = spp.iloc[i]/spp.loc[temp] - 1
            except Exception:
                fac.iloc[i] = np.nan
        self._factor = fac


class BiasFactor(TechFactor):
    # 6日乖离率
    def __init__(self):
        super().__init__('bias')

    def calc(self):
        spp = StockPostPriceFactor().get()
        ls = spp.index  # trading_day_list
        fac = spp.copy()
        for i in range(0, len(spp)):
            try:
                temp = get_day(6, ls, spp.index[i])
                temp2 = get_day(0, ls, spp.index[i])
                fac.iloc[i] = spp.loc[temp2] - spp.loc[temp:temp2].mean()
            except Exception:
                fac.iloc[i] = np.nan
        self._factor = fac


class RSIFactor(TechFactor):
    # 相对强弱指数
    def __init__(self):
        super().__init__('rsi')

    def calc(self):
        spp = StockPostPriceFactor().get()
        ls = spp.index  # trading_day_list
        fac = spp.copy()
        up = spp.copy()
        down = spp.copy()
        up[up.pct_change() < 0] = 0
        down[down.pct_change() > 0] = 0
        for i in range(0, len(spp)):
            try:
                temp = get_day(14, ls, spp.index[i])
                temp2 = get_day(0, ls, spp.index[i])
                up_avg = up.loc[temp:temp2].mean()
                down_avg = down.loc[temp:temp2].mean()
                fac.iloc[i] = up_avg / (up_avg + down_avg) - 1
            except Exception:
                fac.iloc[i] = np.nan
        self._factor = fac


class MixTechFactor(TechFactor):
    # 合成因子
    def __init__(self):
        super().__init__('mixt')
        self._universe: str = 'default'

    # TODO: 这个接口写的不好，暂时先这样
    def set_universe(self, universe: str):
        self._universe = universe

    def calc(self):
        self._factor = ReverseFactor().get_normalized(self._universe) + BiasFactor().get_normalized(self._universe) + RSIFactor().get_normalized(self._universe)
