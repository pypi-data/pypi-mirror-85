
from typing import Optional

import numpy as np
import pandas as pd

from .factor_types import LeverageFactor
from .basic_factors import FloatAssetAvgFactor, FloatDebtAvgFactor, FixAssetAvgFactor, TotalDebtAvgFactor, CashFlowTTMFactor


class FloatRatioFactor(LeverageFactor):
    # 流动比率
    def __init__(self):
        super().__init__('fl_ra')

    def calc(self):
        # 企业的流动资产除以流动负债
        self._factor = FloatAssetAvgFactor().get() / FloatDebtAvgFactor().get().replace({0: np.nan})


class StockDebtRatioFactor(LeverageFactor):
    # 股本债务比
    def __init__(self):
        super().__init__('st_de')

    def calc(self):
        # 企业的净资产除以总债务
        self._factor = FixAssetAvgFactor().get() / TotalDebtAvgFactor().get().replace({0: np.nan})


class CashFlowRatioFactor(LeverageFactor):
    # 营业现金流比率
    def __init__(self):
        super().__init__('cf_r')

    def calc(self):
        # 过去四个季度的经营现金流除以流动负债
        self._factor = CashFlowTTMFactor().get() / FloatDebtAvgFactor().get().replace({0: np.nan})


class MixLeverageFactor(LeverageFactor):
    # 合成因子
    def __init__(self):
        super().__init__('mixl')
        self._universe: str = 'default'

    # TODO: 这个接口写的不好，暂时先这样
    def get(self, universe: str = 'default') -> Optional[pd.DataFrame]:
        self._universe = universe
        self.calc()
        return self._factor

    def calc(self):
        self._factor = FloatRatioFactor().get_normalized(self._universe) + StockDebtRatioFactor().get_normalized(self._universe) + CashFlowRatioFactor().get_normalized(self._universe)
