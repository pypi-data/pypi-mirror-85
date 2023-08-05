
import datetime
from typing import Tuple, List, Optional

import numpy as np
import pandas as pd
import statsmodels.api as sm
from pandas.tseries.offsets import DateOffset

from .derived_factors import DerivedFactor
from .utils import FundHoldStockFactor


class StockFactorApi:

    _DECOMP_RET_DATE_OFFSET = DateOffset(years=1)

    @staticmethod
    def get_stock_factor_ret(factor_names: Tuple[str], universe: str) -> Optional[pd.DataFrame]:
        rets: List[pd.Series] = []
        for one in factor_names:
            try:
                factor = DerivedFactor._registry[one]
            except KeyError as e:
                print(f'[stock_factor_api] invalid stock factor name {one} (err_msg){e} (universe){universe}')
                continue
            f_ret = factor.get_ret(universe=universe)
            if f_ret is not None:
                rets.append(f_ret)
            else:
                print(f'[stock_factor_api] retrieve return of {one} failed (universe){universe}')
        if rets:
            return pd.concat(rets, axis=1)

    @staticmethod
    def decomp_ret(fund_ret: pd.Series, factor_names: Tuple[str], universe: str) -> Optional[pd.Series]:
        ret_rg = StockFactorApi.get_stock_factor_ret(factor_names, universe)
        if ret_rg is None:
            print(f'[stock_factor_api] retrieve return of {factor_names} failed')
            return
        try:
            fund_ret = fund_ret.dropna()
            cal_start_date = (fund_ret.index.array[-1] - StockFactorApi._DECOMP_RET_DATE_OFFSET).date()
            if fund_ret.index.array[0] > cal_start_date:
                print(f'[stock_factor_api] not enough data of fund {fund_ret.name} (start_date){fund_ret.index.array[0]}')
                return
            filtered_fund_ret = fund_ret[fund_ret.index >= cal_start_date]
            if filtered_fund_ret.empty:
                print(f'[stock_factor_api] no data of fund {fund_ret.name} to decomp (start_date){fund_ret.index.array[0]} (end_date){fund_ret.index.array[-1]}')
                return
            rg = filtered_fund_ret.to_frame().join(ret_rg).ffill().dropna()
            Y = rg.iloc[:, 0]
            X = sm.add_constant(rg.iloc[:, 1:])
            model1 = sm.OLS(Y, X)
            resu1 = model1.fit()
            return pd.Series(resu1.params, index=['const']+ret_rg.columns.to_list(), name=fund_ret.name)
        except Exception as e:
            print(f'[stock_factor_api] abnormal error when decomp return (err_msg){e}')
            return

    @staticmethod
    def fac_pos(fund_id: str, factor_names: Tuple[str], report_date: datetime.date) -> Optional[pd.DataFrame]:
        df = FundHoldStockFactor().get()
        if df is None:
            print(f'[fac_pos] failed to get data of fund hold stock')
            return
        df = df[(df.fund_id == fund_id) & (df.datetime == report_date)]
        df = df[df.notna().all(axis=1)]
        if df.empty:
            print(f'[fac_pos] empty df, can not calc (fund_id){fund_id} (report_date){report_date}')
            return

        s_list: List[pd.Series] = []
        try:
            for one in factor_names:
                try:
                    factor = DerivedFactor._registry[one]
                except KeyError as e:
                    print(f'[fac_pos] invalid stock factor name {one} (err_msg){e}')
                    continue
                f_val = factor.get()
                if f_val is None:
                    print(f'[fac_pos] retrieve value of {one} failed')
                    continue
                anjou = []
                weight = []
                for i in range(1, 11):
                    lis = df['rank'+str(i)+'_stock_code'].values
                    mult1 = pd.DataFrame(f_val[lis].iloc[-1])
                    mult1.columns = ['rank'+str(i)+'_fac']
                    mult2 = pd.DataFrame(df['rank'+str(i)+'_stockweight']).set_index(df['rank'+str(i)+'_stock_code'])
                    mult2.columns = ['rank'+str(i)+'_fac']
                    w = mult2.copy()
                    w.index = df.fund_id.to_list()
                    weight.append(w)
                    louis = (mult1 * mult2).replace({np.nan: 0})
                    louis.index = df.fund_id.to_list()
                    anjou.append(louis)
                res = (pd.concat(anjou, axis=1).sum(axis=1) / pd.concat(weight, axis=1).sum(axis=1)).rename(one)
                s_list.append(res)
        except Exception as e:
            print(f'[fac_pos] abnormal error when calc fac pos (err_msg){e}')
            return
        res_df = pd.DataFrame(s_list)
        if res_df.empty:
            return
        return res_df[fund_id]
