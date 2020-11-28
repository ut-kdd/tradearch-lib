from typing import Type

import pandas as pd

from tradearch.core.model import Model, ModelOutputTypes


def generate_model_from_scikit_model(scikit_model_class: Type, model_output_type: ModelOutputTypes) -> Type[Model]:
    class ScikitModel(Model):
        output_type = model_output_type

        def __init__(self, *args, **kwargs):
            super().__init__()
            self.args = args
            self.kwargs = kwargs
            self._scikit_model = None

        def reset(self):
            super().reset()
            self._scikit_model = scikit_model_class(*self.args, **self.kwargs)

        def fit(self, x: pd.DataFrame, y: pd.Series):
            self.reset()
            self._scikit_model.fit(x, y)

        def predict(self, x: pd.DataFrame) -> pd.Series:
            return self._scikit_model.predict(x)

    return ScikitModel
