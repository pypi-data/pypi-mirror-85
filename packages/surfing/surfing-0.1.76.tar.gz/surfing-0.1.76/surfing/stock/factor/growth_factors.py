
import pandas as pd

from .factor_types import GrowthFactor
from .basic_factors import IncomeFactor, AdjNetProfitFactor, CashFlowFactor
from .utils import calc_growth_rate, normalize


class IncomeGrowthFactor(GrowthFactor):
    # 收入增长
    def __init__(self):
        super().__init__('inc_gr')

    def calc(self):
        # 过去四个季度的营业收入增长率
        income = IncomeFactor().get()
        self._factor = income.apply(calc_growth_rate, axis=1, result_type='broadcast', whole_df=income)


class NetProfitOfNonRecurringGoLFactor(GrowthFactor):
    # 扣非后盈利增长
    def __init__(self):
        super().__init__('np_nrgol')

    def calc(self):
        # 过去四个季度扣除非经常性损益后的净利润的增长率
        adj_net_profit = AdjNetProfitFactor().get()
        self._factor = adj_net_profit.apply(calc_growth_rate, axis=1, result_type='broadcast', whole_df=adj_net_profit)


class OperationalCashFlowFactor(GrowthFactor):
    # 经营性现金流增长
    def __init__(self):
        super().__init__('op_cf')

    def calc(self):
        # 企业过去四个季度经营性现金流的增长率
        cash_flow = CashFlowFactor().get()
        self._factor = cash_flow.apply(calc_growth_rate, axis=1, result_type='broadcast', whole_df=cash_flow)


class MixGrowthFactor(GrowthFactor):
    # 合成因子
    def __init__(self):
        super().__init__('mixg')
        self._universe: str = 'default'

    # TODO: 这个接口写的不好，暂时先这样
    def set_universe(self, universe: str):
        self._universe = universe

    def calc(self):
        index = IncomeGrowthFactor().get(self._universe).index
        columns = IncomeGrowthFactor().get(self._universe).columns
        self._factor = pd.DataFrame((normalize(IncomeGrowthFactor().get(self._universe).T) + normalize(NetProfitOfNonRecurringGoLFactor().get(self._universe).T) +
                                    normalize(OperationalCashFlowFactor().get(self._universe).T)).T, index=index, columns=columns)
