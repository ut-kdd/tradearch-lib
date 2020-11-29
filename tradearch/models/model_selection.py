from typing import List

import numpy as np
import pandas as pd

from tradearch.core.model import Model, ModelOutputTypes


class ModelSelectionModel(Model):
    output_type = ModelOutputTypes.CLASSIFICATION

    def __init__(self, selection_models: List[Model], meta_model: Model):
        super().__init__()
        self.selection_models = selection_models
        self.meta_model = meta_model

    def reset(self):
        super().reset()
        self.meta_model.reset()

    def fit(self, x: pd.DataFrame, y: pd.Series):
        self.reset()

        selection_predictions = []
        from_t = y.index.min()
        to_t = y.index.max()
        for j, selection_model in enumerate(self.selection_models):
            predictions = selection_model.predict_by_time(from_t=from_t, to_t=to_t)
            selection_predictions.append(predictions)

        model_y = pd.Series(index=y.index, dtype='int32')
        for i, v in y.iteritems():
            for j, predictions in enumerate(selection_predictions):
                pred = predictions[i]
                if pred == v:
                    model_y.loc[i] = j
                    break
            else:
                model_y.loc[i] = np.nan

        model_y = model_y.dropna()
        mx = x[x.index.isin(model_y.index)]
        self.meta_model.fit(mx, model_y)

    def predict(self, x: pd.DataFrame) -> pd.Series:
        real_y = pd.Series(index=x.index)
        model_y = self.meta_model.predict(x)

        selection_predictions = []
        from_t = x.index.min()
        to_t = x.index.max()
        for j, selection_model in enumerate(self.selection_models):
            predictions = selection_model.predict_by_time(from_t=from_t, to_t=to_t)
            selection_predictions.append(predictions)

        for i, j in model_y.iteritems():
            real_y.loc[i] = selection_predictions[int(j)][i]

        return real_y
