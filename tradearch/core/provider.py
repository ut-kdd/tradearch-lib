from abc import ABC, abstractmethod
from datetime import datetime
from typing import Tuple, Optional, Iterable

import pandas as pd


class Provider(ABC):
    def get_data(self, from_t: Optional[datetime] = None, to_t: Optional[datetime] = None) -> pd.DataFrame:
        dataset = self.get_all_data()

        if from_t is None:
            from_t = dataset.index.min()

        if to_t is None:
            to_t = dataset.index.max()

        dataset = dataset[(dataset.index >= from_t) & (dataset.index <= to_t)]

        return dataset

    def get_date_range(self) -> Tuple[datetime, datetime]:
        dataset = self.get_all_data()
        return dataset.index.min(), dataset.index.max()

    @abstractmethod
    def get_all_data(self) -> pd.DataFrame:
        pass


def get_provider_series(provider: Provider, from_t: datetime, to_t: datetime, column: str) -> pd.Series:
    return provider.get_data(from_t=from_t, to_t=to_t)[column]


def get_provider_dataset(provider: Provider, from_t: datetime, to_t: datetime,
                         columns: Optional[Iterable[str]], slug: Optional[str] = None) -> pd.DataFrame:
    dataset = provider.get_data(from_t=from_t, to_t=to_t)

    if slug:
        dataset = dataset.add_prefix(prefix=slug)

    return dataset[columns if columns is not None else dataset.columns]
