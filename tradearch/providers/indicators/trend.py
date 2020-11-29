import pandas as pd
from ta.trend import SMAIndicator, MACD, PSARIndicator

from tradearch.core.provider import Provider


class SMAIndicatorProvider(Provider):
    def __init__(self, price_provider: Provider, window: int = 14):
        self.price_provider = price_provider
        self.window = window

    def get_all_data(self) -> pd.DataFrame:
        prices = self.price_provider.get_all_data()

        indicator = SMAIndicator(close=prices['adj_close'], window=self.window, fillna=False)

        ret = indicator.sma_indicator().to_frame(name='sma')
        ret['sma_signal'] = 0  # no signal
        ret.loc[ret['sma'] >= prices.loc[prices.index.isin(ret.index), 'adj_close'], 'sma_signal'] = -1  # down trend
        ret.loc[ret['sma'] <= prices.loc[prices.index.isin(ret.index), 'adj_close'], 'sma_signal'] = 1  # up trend

        return ret.dropna()


class MACDIndicatorProvider(Provider):
    def __init__(self, price_provider: Provider, window_slow: int = 26, window_fast: int = 12, window_sign: int = 9):
        self.price_provider = price_provider
        self.window_slow = window_slow
        self.window_fast = window_fast
        self.window_sign = window_sign

    def get_all_data(self) -> pd.DataFrame:
        prices = self.price_provider.get_all_data()

        indicator = MACD(close=prices['adj_close'],
                         window_slow=self.window_slow, window_fast=self.window_fast, window_sign=self.window_sign,
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
