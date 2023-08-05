#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Helper functions primarily for data analysis
"""


__author__ = 'Ross Bonallo'
__license__ = 'MIT Licence'
__version__ = '1.0.3'


import pandas as pd
import numpy as np
from datetime import datetime, timedelta


def seag(_df, period='Y', agg='sum', realign_month=None):
    if isinstance(_df, pd.Series):
        df = pd.DataFrame(_df).copy()
    else:
        df = _df.copy()

    # E.g Sum/Win chart we would like to reset on 1st April. Realign Month = 4.
    realign_day = None
    if realign_month:
        realign_day = datetime(2020, realign_month, 1)
        day_diff = (datetime(2020,1,1,) - datetime(2019, realign_month, 1)).days
        df.index = df.index + timedelta(days=day_diff)

    if agg =='mean':
        agg_func = np.mean
    else:
        agg_func = np.sum

    if period == 'M':
        _df = pd.pivot_table(df, index=df.index.day, columns=df.index.month,
                aggfunc=agg_func, fill_value=np.nan)

    elif period == 'W':
        _df = pd.pivot_table(df, index=df.index.dayofweek, columns=df.index.year,
                aggfunc=agg_func, fill_value=np.nan)

    elif period == 'WA':
        _df = pd.pivot_table(df, index=df.index.week, columns=df.index.year,
                aggfunc=agg_func, fill_value=np.nan)

    elif period == 'Y':
        _df = pd.pivot_table(df, index=df.index.dayofyear, columns=df.index.year,
                aggfunc=agg_func, fill_value=np.nan)

    else:
        raise(Exception('Period {} not available'.format(period)))

    _df = _df.droplevel(0, axis=1).fillna(method='ffill')

    if realign_month:
        dt_index = [realign_day + timedelta(days=i) for i in range(len(_df.index))]
        _df.index = dt_index

        last_column = _df.columns[-1]
        col = _df[last_column]
        _df[last_column] = col[col.index < datetime.today()]

    return _df


def savgolay(df, period=5, order=2):
    from scipy.signal import savgol_filter
    return df.apply(lambda s: savgol_filter(s, period, order))


def annualize(rate,period):
    return ((1. + rate)**period)-1.


def deannualize(rate,period):
    return ((rate + 1.)**(1./period))-1.

