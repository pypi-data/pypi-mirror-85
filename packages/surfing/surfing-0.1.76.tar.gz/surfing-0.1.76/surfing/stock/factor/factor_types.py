
from .derived_factors import DerivedFactor
from ...constant import StockFactorType


class ValueFactor(DerivedFactor):
    # 所有价值因子的基类
    def __init__(self, name):
        super().__init__(f'val/{name}', StockFactorType.VALUE)


class GrowthFactor(DerivedFactor):
    # 所有成长因子的基类
    def __init__(self, name):
        super().__init__(f'gro/{name}', StockFactorType.GROWTH)


class FinQualityFactor(DerivedFactor):
    # 所有财务质量因子的基类
    def __init__(self, name):
        super().__init__(f'fin/{name}', StockFactorType.FIN_QUALITY)


class VolatilityFactor(DerivedFactor):
    # 所有波动率因子的基类
    def __init__(self, name):
        super().__init__(f'vol/{name}', StockFactorType.VOLATILITY)


class ScaleFactor(DerivedFactor):
    # 所有规模因子的基类
    def __init__(self, name):
        super().__init__(f'sca/{name}', StockFactorType.SCALE)


class LeverageFactor(DerivedFactor):
    # 所有杠杆因子的基类
    def __init__(self, name):
        super().__init__(f'lev/{name}', StockFactorType.LEVERAGE)


class MomentumFactor(DerivedFactor):
    # 所有动量因子的基类
    def __init__(self, name):
        super().__init__(f'mom/{name}', StockFactorType.MOMENTUM)


class LiquidityFactor(DerivedFactor):
    # 所有流动性因子的基类
    def __init__(self, name):
        super().__init__(f'liq/{name}', StockFactorType.LIQUIDITY)


class TechFactor(DerivedFactor):
    # 所有技术因子的基类
    def __init__(self, name):
        super().__init__(f'tech/{name}', StockFactorType.TECH)
