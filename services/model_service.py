import mlflow

class ModelService():

    @classmethod
    def load(cls, model_loc, registry_uri="databricks-uc"):
        model_uri = f"models:/{model_loc}"
        mlflow.set_registry_uri(registry_uri)

        python_model = mlflow.pyfunc.load_model(model_uri).unwrap_python_model()
        return python_model
