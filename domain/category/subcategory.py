from domain.category.category import Category


class Subcategory:
    id: int
    name: str
    category: Category

    def __init__(self, id: int, name: str, category: Category):
        self.id = id
        self.name = name
        self.category = category

    def __str__(self):
        return f"id - {self.id} " \
               f"name - {self.name} " \
               f"category - {self.category.__str__()} "
