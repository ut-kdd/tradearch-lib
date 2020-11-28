from typing import Iterable, Dict, Union

import pandas as pd

from tradearch.core.provider import Provider


def lag_provider(provider: Provider, lag_sequence: Union[Iterable[int], Dict[str, Iterable[int]]] = (0, 1)) -> Provider:
    if type(lag_sequence) == list:
        final_lag_sequence = {}
        for column in provider.get_all_data().columns:
            final_lag_sequence[column] = lag_sequence
    else:
        final_lag_sequence = lag_sequence

    class LaggedProvider(Provider):
        def get_all_data(self) -> pd.DataFrame:
            dataset = provider.get_all_data()

            ret = pd.DataFrame()
            for column in final_lag_sequence.keys():
                for i in final_lag_sequence.get(column, []):
                    ret[f'{column}_lagged_{i}' if i > 0 else f'{column}'] = dataset[column].shift(i)

            return ret

    return LaggedProvider()
