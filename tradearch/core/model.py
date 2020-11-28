from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum
from typing import Optional, Iterable

import pandas as pd
from sklearn.metrics import accuracy_score, f1_score, mean_squared_error, mean_absolute_error, r2_score

from .provider import Provider, get_provider_series, get_provider_dataset


class ModelOutputTypes(Enum):
    CLASSIFICATION = 'CLASSIFICATION'
    REGRESSION = 'REGRESSION'


class Model(ABC):
    output_type: ModelOutputTypes = None

    def __init__(self):
        self.input_feature_descriptors = []
        self.input_model_descriptors = []
        self.output_feature_descriptor = None
        self.output_model = None

    def add_input_features(self, provider: Provider, columns: Optional[Iterable[str]] = None,
                           slug: Optional[str] = None):
        self.input_feature_descriptors.append({
            'provider': provider,
            'columns': columns,
            'slug': slug,
        })
        return self

    def add_input_model(self, model: Model, slug: Optional[str] = None):
        self.input_model_descriptors.append({
            'model': model,
            'slug': slug,
        })
        return self

    def set_output_feature(self, provider: Provider, column: str):
        self.output_model = None
        self.output_feature_descriptor = {
            'provider': provider,
            'column': column,
        }
        return self

    def set_output_model(self, model: Model):
        self.output_feature_descriptor = None
        self.output_model = model
        return self

    def fit_by_time(self, from_t: datetime, to_t: datetime):
        input_dataset = self.get_input_dataset(from_t=from_t, to_t=to_t)
        output_dataset = self.get_output_dataset(from_t=from_t, to_t=to_t)

        input_dataset = input_dataset[input_dataset.index.isin(output_dataset.index)]
        output_dataset = output_dataset[output_dataset.index.isin(input_dataset.index)].reindex(input_dataset.index)

        self.fit(input_dataset, output_dataset)

    def predict_by_time(self, from_t: datetime, to_t: datetime) -> pd.Series:
        input_dataset = self.get_input_dataset(from_t=from_t, to_t=to_t)
        output_dataset = pd.Series(self.predict(input_dataset), index=input_dataset.index)
        return output_dataset

    def measure_by_time(self, from_t: datetime, to_t: datetime) -> dict:
        predicted_output = self.predict_by_time(from_t=from_t, to_t=to_t)
        expected_output = self.get_output_dataset(from_t=from_t, to_t=to_t)

        expected_output = expected_output[expected_output.index.isin(predicted_output.index)] \
            .reindex(predicted_output.index)

        if self.output_type == ModelOutputTypes.CLASSIFICATION:
            return {
                'accuracy': accuracy_score(expected_output, predicted_output),
                'f1_score': f1_score(expected_output, predicted_output),
            }
        elif self.output_type == ModelOutputTypes.REGRESSION:
            return {
                'mae': mean_absolute_error(expected_output, predicted_output),
                'mse': mean_squared_error(expected_output, predicted_output),
                'r2_score': r2_score(expected_output, predicted_output),
            }

        raise Exception('this output type does not support measure')

    def get_input_dataset(self, from_t: datetime, to_t: datetime) -> pd.DataFrame:
        input_datasets = []
        for feature_descriptor in self.input_feature_descriptors:
            dataset = get_provider_dataset(provider=feature_descriptor.get('provider'),
                                           from_t=from_t, to_t=to_t,
                                           columns=feature_descriptor.get('columns'),
                                           slug=feature_descriptor.get('slug'))
            input_datasets.append(dataset)

        for model_descriptor in self.input_model_descriptors:
            dataset = get_model_dataset(model=model_descriptor.get('model'),
                                        from_t=from_t, to_t=to_t,
                                        slug=model_descriptor.get('slug'))
            input_datasets.append(dataset)

        if not input_datasets:
            return pd.DataFrame()

        ret = input_datasets[0]
        for dataset in input_datasets:
            ret = pd.merge(ret, dataset, left_index=True, right_index=True)

        ret = ret.dropna()

        return ret

    def get_output_dataset(self, from_t: datetime, to_t: datetime) -> pd.Series:
        if self.output_model is not None:
            return get_model_series(model=self.output_model, from_t=from_t, to_t=to_t)

        if self.output_feature_descriptor is not None:
            return get_provider_series(provider=self.output_feature_descriptor.get('provider'),
                                       from_t=from_t, to_t=to_t,
                                       column=self.output_feature_descriptor.get('column'))

        raise Exception('no output is set on model')

    def get_layers(self) -> Iterable[Iterable[Model]]:
        layers = [[self]]

        while True:
            layer = []
            for model in layers[-1]:
                layer.extend([x.get('model') for x in model.input_model_descriptors])

            if not layer:
                break

            layers.append(layer)

        return reversed(layers)

    def reset(self):
        for model_descriptor in self.input_model_descriptors:
            model_descriptor.get('model').reset()

    @abstractmethod
    def fit(self, x: pd.DataFrame, y: pd.Series):
        raise NotImplementedError('fit method is not implemented')

    @abstractmethod
    def predict(self, x: pd.DataFrame) -> pd.Series:
        raise NotImplementedError('predict method is not implemented')


def get_model_series(model: Model, from_t: datetime, to_t: datetime) -> pd.Series:
    return model.predict_by_time(from_t=from_t, to_t=to_t)


def get_model_dataset(model: Model, from_t: datetime, to_t: datetime, slug: Optional[str] = None) -> pd.DataFrame:
    return model.predict_by_time(from_t=from_t, to_t=to_t).to_frame(slug if slug else 'prediction')
