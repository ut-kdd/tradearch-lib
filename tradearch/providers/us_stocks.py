import math
from pathlib import Path
from typing import Iterable, Dict

import pandas as pd

from tradearch.core.provider import Provider


class USStockOHCPProvider(Provider):
    def __init__(self, symbol: str):
        super().__init__()
        self.symbol = symbol

    def get_all_data(self) -> pd.DataFrame:
        file_path = Path(__file__).parent.parent.joinpath(f'data/us_stocks/{self.symbol}.csv')

        dataset = pd.read_csv(file_path, parse_dates=True, index_col='date')
        dataset = dataset.dropna()
        return dataset


class USStockDiffProvider(Provider):
    def __init__(self, symbol: str, n_days: int = 1):
        super().__init__()
        self.symbol = symbol
        self.n_days = n_days

    def get_all_data(self) -> pd.DataFrame:
        ohcp_dataset = USStockOHCPProvider(symbol=self.symbol).get_all_data()

        dataset = ohcp_dataset.diff(self.n_days)
        dataset = dataset.dropna()
        return dataset


class USStockDiffQuantizedProvider(Provider):
    def __init__(self, symbol: str, bins: Dict[str, Iterable[float]],
                 labels: Dict[str, Iterable[int]], n_days: int = 1):
        super().__init__()
        self.symbol = symbol
        self.bins = bins
        self.labels = labels
        self.n_days = n_days

    def get_all_data(self) -> pd.DataFrame:
        diff_dataset = USStockDiffProvider(symbol=self.symbol, n_days=self.n_days).get_all_data()

        dataset = pd.DataFrame()
        for col in diff_dataset.columns:
            dataset[col] = pd.cut(diff_dataset[col], bins=self.bins.get(col), labels=self.labels.get(col))
        dataset = dataset.dropna()
        return dataset


class USStockMovementProvider(Provider):
    def __init__(self, symbol: str, n_days: int = 1):
        super().__init__()
        self.symbol = symbol
        self.n_days = n_days

    def get_all_data(self) -> pd.DataFrame:
        bins = {
            'open': [-math.inf, 0, math.inf],
            'close': [-math.inf, 0, math.inf],
            'high': [-math.inf, 0, math.inf],
            'low': [-math.inf, 0, math.inf],
            'adj_close': [-math.inf, 0, math.inf],
            'volume': [-math.inf, 0, math.inf],
        }
        labels = {
            'open': [-1, 1],
            'close': [-1, 1],
            'high': [-1, 1],
            'low': [-1, 1],
            'adj_close': [-1, 1],
            'volume': [-1, 1],
        }
        dataset = USStockDiffQuantizedProvider(symbol=self.symbol, bins=bins, labels=labels,
                                               n_days=self.n_days).get_all_data()
        return dataset
