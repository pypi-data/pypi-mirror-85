from .model_wrapper import ModelWrapper


# noinspection PyProtectedMember,PyPackageRequirements
def _load_pyfunc(path: str):
    import mlflow

    model = mlflow.sklearn._load_pyfunc(path)
    return ModelWrapper(model)
