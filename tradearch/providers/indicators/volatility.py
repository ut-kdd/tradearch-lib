import pandas as pd
from ta.volatility import BollingerBands

from tradearch.core.provider import Provider


class BollingerBandsIndicatorProvider(Provider):
    def __init__(self, price_provider: Provider, n: int = 20, n_dev: int = 2):
        self.price_provider = price_provider
        self.n = n
        self.n_dev = n_dev

    def get_all_data(self) -> pd.DataFrame:
        prices = self.price_provider.get_all_data()

        indicator = BollingerBands(close=prices['adj_close'], n=self.n, ndev=self.n_dev,
                                   fillna=False)

        ret = indicator.bollinger_hband().to_frame(name='bollinger_hband')
        ret['bollinger_lband'] = indicator.bollinger_lband()
        ret['bollinger_mavg'] = indicator.bollinger_mavg()
        ret['bollinger_pband'] = indicator.bollinger_pband()
        ret['bollinger_wband'] = indicator.bollinger_wband()

        return ret.dropna()
