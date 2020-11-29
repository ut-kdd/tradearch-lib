from sklearn.ensemble import RandomForestClassifier as _RandomForestClassifier, \
    AdaBoostClassifier as _AdaBoostClassifier, \
    GradientBoostingClassifier as _GradientBoostingClassifier, \
    BaggingClassifier as _BaggingClassifier
from sklearn.linear_model import LogisticRegression as _LogisticRegression, \
    SGDClassifier as _SGDClassifier
from sklearn.svm import SVC as _SVC, LinearSVC as _LinearSVC

from tradearch.core import ModelOutputTypes
from tradearch.helpers import generate_model_from_scikit_model

RandomForestClassifier = generate_model_from_scikit_model(scikit_model_class=_RandomForestClassifier,
                                                          model_output_type=ModelOutputTypes.CLASSIFICATION)

AdaBoostClassifier = generate_model_from_scikit_model(scikit_model_class=_AdaBoostClassifier,
                                                      model_output_type=ModelOutputTypes.CLASSIFICATION)

GradientBoostingClassifier = generate_model_from_scikit_model(scikit_model_class=_GradientBoostingClassifier,
                                                              model_output_type=ModelOutputTypes.CLASSIFICATION)

BaggingClassifier = generate_model_from_scikit_model(scikit_model_class=_BaggingClassifier,
                                                     model_output_type=ModelOutputTypes.CLASSIFICATION)

SVC = generate_model_from_scikit_model(scikit_model_class=_SVC,
                                       model_output_type=ModelOutputTypes.CLASSIFICATION)

LinearSVC = generate_model_from_scikit_model(scikit_model_class=_LinearSVC,
                                             model_output_type=ModelOutputTypes.CLASSIFICATION)

LogisticRegression = generate_model_from_scikit_model(scikit_model_class=_LogisticRegression,
                                                      model_output_type=ModelOutputTypes.CLASSIFICATION)

SGDClassifier = generate_model_from_scikit_model(scikit_model_class=_SGDClassifier,
                                                 model_output_type=ModelOutputTypes.CLASSIFICATION)
