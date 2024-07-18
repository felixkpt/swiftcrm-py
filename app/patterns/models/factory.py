class ModelFactory:
    def create_instance(self, model_class, **kwargs):
        instance = model_class(**kwargs)
        return instance
