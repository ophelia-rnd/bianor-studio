import mlflow

from sklearn.base import BaseEstimator, TransformerMixin
from minisom_representation import SomRepresentation

class ModelService():

    @classmethod
    def load(cls, model_loc, registry_uri="databricks-uc"):
        model_uri = f"models:/{model_loc}"
        mlflow.set_registry_uri(registry_uri)
        python_model = mlflow.pyfunc.load_model(model_uri).unwrap_python_model()

        assert hasattr(python_model, "model") and isinstance(python_model.model, SomRepresentation),\
            "Attribute `model` of the loaded model is not set or is not a SomRepresentation instance"

        assert (hasattr(python_model, "scaler")
                and isinstance(python_model.scaler, (TransformerMixin, BaseEstimator))
                and hasattr(python_model.scaler, "transform")),\
                "Attribute `scaler` of the loaded model is not set or is not a valid sklearn transformer"

        return python_model
