
from typing import Optional, Dict
import statsmodels.api as sm
import numpy as np
import pandas as pd
import scipy.stats as st

from ...constant import StockFactorType
from .base import Factor
from .basic_factors import StockPostPriceFactor
from .utils import get_quarterly_tradingday_list


class DerivedFactor(Factor):

    _registry = {}

    def __init__(self, name, f_type: StockFactorType):
        super().__init__(name, f_type)
        # 这里我们将每一个universe下的因子值都存下来
        self._factor_ret: Dict[str, pd.DataFrame] = {}

    def get_ret(self, universe='default') -> Optional[pd.DataFrame]:
        try:
            return self._factor_ret[universe]
        except KeyError:
            return self._load_ret(universe)

    def save_ret(self, universe='default') -> bool:
        try:
            self._factor_ret[universe].to_parquet(self._get_s3_factor_ret_uri(universe), compression='gzip')
            return True
        except KeyError:
            return False

    def register(self):
        DerivedFactor._registry[self.name] = self

    def calc_ret(self, universe='default', n=5) -> pd.DataFrame:
        '''
        Name: calc_ret
        Input: A DataFrame of factor; number of groups.
        Output: The factor return series of F1-Fn portfolio.
        '''
        ret_list = []
        dt_list = []
        isNaN = True
        factor = self.get(universe=universe)
        # 计算收益
        spp_factor = StockPostPriceFactor().get()
        ret = spp_factor.apply(np.log).diff()
        tradingday_list = get_quarterly_tradingday_list()
        for i in range(0, len(factor)):
            dt_list.append(factor.index[i])
            if len(factor.iloc[i].dropna()) == 0:
                ret_list.append(np.nan)
            elif isNaN:
                F1_bound = factor.iloc[i].dropna().quantile(1-1/n)
                Fn_bound = factor.iloc[i].dropna().quantile(1/n)
                F1_set = factor.iloc[i][factor.iloc[i] > F1_bound].index
                Fn_set = factor.iloc[i][factor.iloc[i] < Fn_bound].index
                ret_list.append(np.nan)
                isNaN = False
            elif factor.index[i] in tradingday_list:
                F1_ret = ret.iloc[i][F1_set].mean()
                Fn_ret = ret.iloc[i][Fn_set].mean()
                ret_list.append(F1_ret - Fn_ret)

                F1_bound = factor.iloc[i-1].dropna().quantile(1-1/n)
                Fn_bound = factor.iloc[i-1].dropna().quantile(1/n)
                F1_set = factor.iloc[i-1][factor.iloc[i-1] > F1_bound].index
                Fn_set = factor.iloc[i-1][factor.iloc[i-1] < Fn_bound].index
            else:
                F1_ret = ret.iloc[i][F1_set].mean()
                Fn_ret = ret.iloc[i][Fn_set].mean()
                ret_list.append(F1_ret - Fn_ret)

        self._factor_ret[universe] = pd.DataFrame(ret_list, index=dt_list)
        self._factor_ret[universe].columns = [self.name]

    # @staticmethod
    # def print_table(table, name=None, fmt=None):
    #     """
    #     Pretty print a pandas DataFrame.
    #     Uses HTML output if running inside Jupyter Notebook, otherwise
    #     formatted text output.
    #     Parameters
    #     ----------
    #     table : pd.Series or pd.DataFrame
    #         Table to pretty-print.
    #     name : str, optional
    #         Table name to display in upper left corner.
    #     fmt : str, optional
    #         Formatter to use for displaying table elements.
    #         E.g. '{0:.2f}%' for displaying 100 as '100.00%'.
    #         Restores original setting after displaying.
    #     """
    #     if isinstance(table, pd.Series):
    #         table = pd.DataFrame(table)

    #     if isinstance(table, pd.DataFrame):
    #         table.columns.name = name

    #     prev_option = pd.get_option('display.float_format')
    #     if fmt is not None:
    #         pd.set_option('display.float_format', lambda x: fmt.format(x))

    #     # display(table)

    #     if fmt is not None:
    #         pd.set_option('display.float_format', prev_option)

    def ic_analysis(self, lis=[1,5,10]):
        ic_total = []
        pv_total = []
        for num in lis:
            ic_list = []
            pv_list = []
            factor = self.get()
            ret_table = StockPostPriceFactor().get().apply(np.log).diff()
            length = len(ret_table)
            for i in range(num, length):
                temp = pd.concat([factor.iloc[i-num], ret_table.iloc[i]], axis=1).dropna()
                ic_list.append(st.spearmanr(temp.iloc[:,0], temp.iloc[:,1]).correlation)
                pv_list.append(st.spearmanr(temp.iloc[:,0], temp.iloc[:,1]).pvalue)
            df = pd.DataFrame([ic_list,pv_list])
            df = df.T
            df.columns = ['ic', 'pvalue']
            ic_array = df.set_index(ret_table.index[num:]) 
            ic_total.append(ic_array.ic)
            pv_total.append(ic_array.pvalue)
        ic_data = pd.concat(ic_total, axis=1)
        self.ic_array = ic_array
        ic_summary_table = pd.DataFrame()
        ic_summary_table["IC Mean"] = ic_data.mean()
        ic_summary_table["IC Std."] = ic_data.std()
        ic_summary_table["Risk-Adjusted IC"] = ic_data.mean() / ic_data.std()
        t_stat, p_value = st.ttest_1samp(ic_data, 0, nan_policy='omit')
        ic_summary_table["t-stat(IC)"] = t_stat
        ic_summary_table["p-value(IC)"] = p_value
        ic_summary_table["IC Skew"] = st.skew(ic_data, nan_policy='omit')
        ic_summary_table["IC Kurtosis"] = st.kurtosis(ic_data, nan_policy='omit')
        #ic_summary_table.columns = lis
        self.ic_summary = ic_summary_table
        self.ic_summary.index = lis
        print("Information Analysis")
        #print(self.ic_summary)
        # self.print_table(ic_summary_table.apply(lambda x: x.round(5)).T)

    def ret_analysis(self, lis = [1,5,10]):
        ret = StockPostPriceFactor().get().apply(np.log).diff()
        factor = self.get()
        ret_total = []
        for num in lis:
            b_list = []
            for i in range(len(ret)-num):
                X = sm.add_constant(factor.iloc[i].dropna())
                Y = (ret.iloc[i+num].dropna())
                X.columns = ['const', 'factor']
                idx = (set(Y.index.values) & set(X.index.values))
                model = sm.WLS(Y.loc[idx],X.loc[idx])
                resu = model.fit()
                b_list.append(resu.params)
            qwq = pd.DataFrame(b_list)
            ret_total.append(qwq.factor)
        ret_data = pd.concat(ret_total, axis=1)
        ret_summary_table = pd.DataFrame()
        ret_summary_table["Annualized Return"] = ret_data.mean()*240
        ret_summary_table["Annualized Vol"] = ret_data.std()*np.sqrt(240)
        ret_summary_table["Sharpe Ratio"] = ret_data.mean() / ret_data.std()
        t_stat, p_value = st.ttest_1samp(ret_data, 0, nan_policy='omit')
        ret_summary_table["t-stat(Daily Return)"] = t_stat
        ret_summary_table["p-value(Daily Return)"] = p_value
        ret_summary_table["Return Skew"] = st.skew(ret_data, nan_policy='omit')
        ret_summary_table["Return Kurtosis"] = st.kurtosis(ret_data, nan_policy='omit') 
        self.ret_summary = ret_summary_table
        self.ret_summary.index = lis
        print("Information Analysis")
        #print(self.ic_summary)
        # self.print_table(ret_summary_table.apply(lambda x: x.round(5)).T)

    



    def _load_ret(self, universe = 'default') -> Optional[pd.DataFrame]:
        try:
            self._factor_ret[universe]: pd.DataFrame = pd.read_parquet(self._get_s3_factor_ret_uri(universe))
        except Exception as e:
            print(f'retrieve ret from s3 failed, (err_msg){e}; try to re-calc')
            self.calc_ret(universe)
        return self._factor_ret[universe]
