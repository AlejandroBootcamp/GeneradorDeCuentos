

class ModelFactory:
    _registry = {}

    #Esto permite un registro dinamico de modelos.
    @classmethod
    def register(cls, model_type: str):
        def wrapper(model_class):
            cls._registry[model_type] = model_class
            return model_class
        return wrapper

    @classmethod
    def create_model(cls, model_type: str, *args, **kwargs):
        if model_type not in cls._registry:
            raise ValueError(f"Modelo no registrado: {model_type}")
        class_ins = cls._registry[model_type](*args, **kwargs)
        return  class_ins