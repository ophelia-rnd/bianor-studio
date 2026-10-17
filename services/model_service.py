import os
from pathlib import Path

import mlflow
from sklearn.base import BaseEstimator, TransformerMixin
from minisom_representation import SomRepresentation

from services.backend import is_local, local_root

_MLFLOW_URI_PREFIXES = ("models:", "runs:", "file:")


class ModelService:

    @classmethod
    def _configure_local_mlflow(cls):
        tracking_uri = os.getenv("MLFLOW_TRACKING_URI")
        if tracking_uri:
            mlflow.set_tracking_uri(tracking_uri)
        registry_uri = os.getenv("MLFLOW_REGISTRY_URI")
        if registry_uri:
            mlflow.set_registry_uri(registry_uri)

    @classmethod
    def _resolve_uri(cls, model_loc, registry_uri):
        if model_loc.startswith(_MLFLOW_URI_PREFIXES):
            if is_local():
                cls._configure_local_mlflow()
            else:
                mlflow.set_registry_uri(registry_uri)
            return model_loc

        if is_local():
            cls._configure_local_mlflow()
            path = Path(model_loc).expanduser()
            if not path.is_absolute():
                path = local_root() / path
            path = path.resolve()
            assert path.is_dir(), (
                f"Local MLflow model directory not found: {path}. "
                "Copy a logged MLflow model folder (containing MLmodel) to this path."
            )
            assert (path / "MLmodel").is_file(), (
                f"Not an MLflow model directory (missing MLmodel): {path}"
            )
            return str(path)

        mlflow.set_registry_uri(registry_uri)
        return f"models:/{model_loc}"

    @classmethod
    def load(cls, model_loc, registry_uri="databricks-uc"):
        model_uri = cls._resolve_uri(model_loc, registry_uri)
        python_model = mlflow.pyfunc.load_model(model_uri).unwrap_python_model()

        assert hasattr(python_model, "model") and isinstance(python_model.model, SomRepresentation),\
            "Attribute `model` of the loaded model is not set or is not a SomRepresentation instance"

        assert (hasattr(python_model, "scaler")
                and isinstance(python_model.scaler, (TransformerMixin, BaseEstimator))
                and hasattr(python_model.scaler, "transform")),\
                "Attribute `scaler` of the loaded model is not set or is not a valid sklearn transformer"

        return python_model
