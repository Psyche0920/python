class Plant:
    def __init__(self, name, height, age):
        self.name = name
        self.height = height
        self.age = age


class Flower(Plant):
    def __init__(self, name, height, age, color):
        super().__init__(name, height, age)
        self.color = color

    def describe(self):
        print(
            f"{self.name} (Flower): {self.height}cm, {self.age} days, "
            f"{self.color} color"
        )

    def bloom(self):
        print(f"{self.name} is blooming beautifully!")


class Tree(Plant):
    def __init__(self, name, height, age, trunk_diameter):
        super().__init__(name, height, age)
        self.trunk_diameter = trunk_diameter

    def describe(self):
        print(
            f"{self.name} (Tree): {self.height}cm, {self.age} days, "
            f"{self.trunk_diameter}cm diameter"
        )

    def produce_shade(self):
        shade_area = (self.height / 500) * 78
        print(f"{self.name} provides {shade_area:.0f} square meters of shade")


class Vegetable(Plant):
    def __init__(self, name, height, age, harvest_season, nutritional_value):
        super().__init__(name, height, age)
        self.harvest_season = harvest_season
        self.nutritional_value = nutritional_value

    def describe(self):
        print(
            f"{self.name} (Vegetable): {self.height}cm, {self.age} days, "
            f"{self.harvest_season} harvest"
        )

    def nutrition_info(self):
        print(f"{self.name} is rich in {self.nutritional_value}")


if __name__ == "__main__":
    print("=== Garden Plant Types ===")
    print()
    rose = Flower("Rose", 25, 30, "red")
    tulip = Flower("Tulip", 15, 20, "yellow")
    oak = Tree("Oak", 500, 1825, 50)
    maple = Tree("Maple", 300, 730, 30)
    tomato = Vegetable("Tomato", 80, 90, "summer", "vitamin C")
    carrot = Vegetable("Carrot", 20, 60, "fall", "vitamin A")

    rose.describe()
    rose.bloom()
    print()
    tulip.describe()
    tulip.bloom()
    print()
    oak.describe()
    oak.produce_shade()
    print()
    maple.describe()
    maple.produce_shade()
    print()
    tomato.describe()
    tomato.nutrition_info()
    print()
    carrot.describe()
    carrot.nutrition_info()
