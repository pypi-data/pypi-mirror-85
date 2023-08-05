"""
The MIT License

Copyright (c) 2018-2020 Mark Douthwaite
"""

import json
from typing import IO, Any, Union

import h5py
from numpy import float64, ndarray, ndim, squeeze
from sklearn import linear_model
from sklearn.base import ClassifierMixin, RegressorMixin
from typing_extensions import Protocol


__version__ = "0.0.1b1"


class LinearModel(Protocol):
    """Protocol defining expected interface of LinearModels in py-lingo."""

    coef_: ndarray
    intercept_: Union[float64, ndarray]

    def get_params(self):
        ...

    def set_params(self, **params: Any):
        ...


def dump(model: LinearModel, file: Union[str, IO]) -> None:
    """
    Dump a Scikit-Learn LinearModel to a HDF5 file.

    Parameters
    ----------
    model: LinearModel
        Your Scikit-Learn-compliant linear model.
    file: str or IO
        A filename or file-like object indicating where you'd like to dump your model!

    Returns
    -------
    None

    """

    with h5py.File(file, "w") as file:
        group = file.create_group("model")
        theta = group.create_dataset("theta", data=model.coef_.flatten())
        intercept = group.create_dataset("intercept", data=model.intercept_.flatten())

        coef = model.coef_
        inter = model.intercept_

        n = ndim(coef)
        print(n, coef.shape, intercept.shape)
        # can this rely on reshaping data instead?
        if n > 1:
            coef_shape = coef.shape
            intercept_shape = (1, intercept.shape[0])
        elif n == 1:
            coef_shape = (1, coef.shape[0])
            intercept_shape = (1, 1)
        else:
            coef_shape = (1, 1)
            intercept_shape = (1, 1)

        theta.attrs["n"] = coef_shape[0]
        theta.attrs["m"] = coef_shape[1]

        intercept.attrs["n"] = intercept_shape[0]
        intercept.attrs["m"] = intercept_shape[1]

        group.attrs["params"] = json.dumps(model.get_params())  # str
        group.attrs["estimatorName"] = type(model).__name__  # str

        if isinstance(model, RegressorMixin):
            group.attrs["estimatorType"] = "regressor"
        elif isinstance(model, ClassifierMixin):
            group.attrs["estimatorType"] = "classifier"
        else:
            raise TypeError("Unsupported model type.")


def load(filename: Union[str, IO]) -> LinearModel:
    """
    Load a py-lingo-formatted Scikit-Learn model from a HDF5 file.

    Parameters
    ----------
    filename: str, file-like
        A filename or file-like object indicating where you'd like to dump your model!

    Returns
    -------
    LinearModel
        Et voila, your model!

    """

    with h5py.File(filename, "r") as file:
        model_data = file["model"]
        theta_data = model_data["theta"]
        intercept_data = model_data["intercept"]
        params = json.loads(model_data.attrs["params"])

        theta = theta_data[()].reshape(theta_data.attrs["n"], theta_data.attrs["m"])
        intercept = intercept_data[()].reshape(
            intercept_data.attrs["n"], intercept_data.attrs["m"]
        )

        model_type = getattr(linear_model, model_data.attrs["estimatorName"])
        model = model_type()
        model.set_params(**params)
        model.coef_ = squeeze(theta)
        model.intercept_ = squeeze(intercept)

    return model
