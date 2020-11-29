import pandas as pd
from ta.trend import SMAIndicator, MACD, PSARIndicator

from tradearch.core.provider import Provider


class SMAIndicatorProvider(Provider):
    def __init__(self, price_provider: Provider, n: int = 14):
        self.price_provider = price_provider
        self.n = n

    def get_all_data(self) -> pd.DataFrame:
        prices = self.price_provider.get_all_data()

        indicator = SMAIndicator(close=prices['adj_close'], n=self.n, fillna=False)

        ret = indicator.sma_indicator().to_frame(name='sma')
        ret['sma_signal'] = 0  # no signal
        ret.loc[ret['sma'] >= prices.loc[prices.index.isin(ret.index), 'adj_close'], 'sma_signal'] = -1  # down trend
        ret.loc[ret['sma'] <= prices.loc[prices.index.isin(ret.index), 'adj_close'], 'sma_signal'] = 1  # up trend

        return ret.dropna()


class MACDIndicatorProvider(Provider):
    def __init__(self, price_provider: Provider, n_slow: int = 26, n_fast: int = 12, n_sign: int = 9):
        self.price_provider = price_provider
        self.n_slow = n_slow
        self.n_fast = n_fast
        self.n_sign = n_sign

    def get_all_data(self) -> pd.DataFrame:
        prices = self.price_provider.get_all_data()

        indicator = MACD(close=prices['adj_close'],
                         n_slow=self.n_slow, n_fast=self.n_fast, n_sign=self.n_sign,
                         fillna=False)

        ret = indicator.macd().to_frame(name='macd')
        ret['macd_sig'] = indicator.macd_signal()
        ret['macd_diff'] = indicator.macd_diff()

        return ret.dropna()


class PSARIndicatorProvider(Provider):
    def __init__(self, price_provider: Provider, step: float = 0.02, max_step: int = 0.2):
        self.price_provider = price_provider
        self.step = step
        self.max_step = max_step

    def get_all_data(self) -> pd.DataFrame:
        prices = self.price_provider.get_all_data()

        indicator = PSARIndicator(close=prices['close'], low=prices['low'], high=prices['high'],
                                  step=self.step, max_step=self.max_step, fillna=False)

        ret = indicator.psar().to_frame(name='psar')
        ret['psar_signal'] = 0  # no signal
        ret.loc[ret['psar'] >= prices.loc[prices.index.isin(ret.index), 'close'], 'psar_signal'] = -1  # down trend
        ret.loc[ret['psar'] <= prices.loc[prices.index.isin(ret.index), 'close'], 'psar_signal'] = 1  # up trend

        return ret.dropna()
