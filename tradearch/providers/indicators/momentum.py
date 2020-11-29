import pandas as pd
from ta.momentum import RSIIndicator

from tradearch.core.provider import Provider


class RSIIndicatorProvider(Provider):
    def __init__(self, price_provider: Provider, window: int = 14, upper_threshold: int = 70,
                 lower_threshold: int = 30):
        self.price_provider = price_provider
        self.window = window
        self.upper_threshold = upper_threshold
        self.lower_threshold = lower_threshold

    def get_all_data(self) -> pd.DataFrame:
        prices = self.price_provider.get_all_data()

        rsi_indicator = RSIIndicator(close=prices['adj_close'], window=self.window, fillna=False)

        ret = rsi_indicator.rsi().to_frame(name='rsi')
        ret['rsi_signal'] = 0  # no signal
        ret.loc[ret['rsi'] >= self.upper_threshold, 'rsi_signal'] = 1  # overbought
        ret.loc[ret['rsi'] <= self.lower_threshold, 'rsi_signal'] = -1  # oversold

        return ret.dropna()
