from faker import Faker


class BaseFactory:
    faker = Faker()
    model = None
    data = {}

    def __init__(self):
        # Define initial data
        pass

    def create(self):
        model = self.model(**self.data)
        model.save()
        return model
