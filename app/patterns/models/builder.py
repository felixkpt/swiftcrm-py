class ModelBuilder:
    def __init__(self, model_class):
        self.model_class = model_class
        self.data = {}

    def set_field(self, key, value):
        self.data[key] = value
        return self

    def build(self):
        return self.model_class(**self.data)
