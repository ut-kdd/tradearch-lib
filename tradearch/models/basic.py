from sklearn.ensemble import RandomForestClassifier as _RandomForestClassifier

from tradearch.core import ModelOutputTypes
from tradearch.helpers import generate_model_from_scikit_model

RandomForestClassifier = generate_model_from_scikit_model(scikit_model_class=_RandomForestClassifier,
                                                          model_output_type=ModelOutputTypes.CLASSIFICATION)
