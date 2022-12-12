from moreview.factories import BaseFactory

from .models import Movie, Tag

class TagFactory(BaseFactory):
    model = Tag

    def __init__(self):
        super().__init__()

        self.data={
            "name":"幽默",
        }

class MovieFactory(BaseFactory):
    model = Movie

    def __init__(self):
        super().__init__()

        self.data = {
            "name":self.faker.name(),
            "content": self.faker.text(),
            "official_site": self.faker.url(),
            "time": self.faker.random_int(100, 200),
            "image": self.faker.file_name(category="image"),
            "grade": self.faker.random_element(
                elements=("普遍級", "保護級", "輔12級", "輔15級", "限制級")
            ),
            "date_released": self.faker.date(),
        }
