class Plant:
    def __init__(self, name, height):
        self.name = name
        self.height = height

    def grow(self):
        self.height += 1
        return 1

    def display(self):
        return f"{self.name}: {self.height}cm"


class FloweringPlant(Plant):
    def __init__(self, name, height, color):
        super().__init__(name, height)
        self.color = color
        self.is_blooming = True

    def bloom_status(self):
        return "blooming" if self.is_blooming else "not blooming"

    def display(self):
        base = super().display()
        return f"{base}, {self.color} flowers ({self.bloom_status()})"


class PrizeFlower(FloweringPlant):
    def __init__(self, name, height, color, points):
        super().__init__(name, height, color)
        self.points = points

    def display(self):
        base = super().display()
        return f"{base}, Prize points: {self.points}"


class GardenStats:
    @classmethod
    def count_plant_types(cls, plants):
        counts = {"regular": 0, "flowering": 0, "prize": 0}
        for plant in plants:
            if isinstance(plant, PrizeFlower):
                counts["prize"] += 1
            elif isinstance(plant, FloweringPlant):
                counts["flowering"] += 1
            else:
                counts["regular"] += 1
        return counts


class GardenManager:
    total_gardens = 0
    all_gardens = []

    def __init__(self, owner):
        self.owner = owner
        self.plants = []
        GardenManager.total_gardens += 1
        GardenManager.all_gardens.append(self)

    def add_plant(self, plant):
        self.plants.append(plant)
        print(f"Added {plant.name} to {self.owner}'s garden")

    def grow_all(self):
        print(f"\n{self.owner} is helping all plants grow...")
        self.total_growth = 0
        for plant in self.plants:
            growth = plant.grow()
            self.total_growth += growth
            print(f"{plant.name} grew {growth}cm")

    def get_plant_count(self):
        count = 0
        for _ in self.plants:
            count += 1
        return count

    def generate_report(self):
        print(f"\n=== {self.owner}'s Garden Report ===")
        print("Plants in garden:")
        for plant in self.plants:
            print(f"- {plant.display()}")
        plant_count = self.get_plant_count()
        plant_counts = GardenStats.count_plant_types(self.plants)
        print(
            f"\nPlants added: {plant_count}, "
            f"Total growth: {self.total_growth}cm"
        )
        print(
            f"Plant types: {plant_counts['regular']} regular, "
            f"{plant_counts['flowering']} flowering, "
            f"{plant_counts['prize']} prize flowers"
        )

    @classmethod
    def get_total_gardens(cls):
        return cls.total_gardens

    @classmethod
    def create_garden_network(cls):
        return f"Garden network: {cls.total_gardens} gardens connected"

    @staticmethod
    def validate_height(h):
        return h >= 0


if __name__ == "__main__":
    print("=== Garden Management System Demo ===\n")
    alice_garden = GardenManager("Alice")
    alice_garden.add_plant(Plant("Oak Tree", 100))
    alice_garden.add_plant(FloweringPlant("Rose", 25, "red"))
    alice_garden.add_plant(PrizeFlower("Sunflower", 50, "yellow", 10))
    alice_garden.grow_all()
    alice_garden.generate_report()
    print(f"\nHeight validation test: {GardenManager.validate_height(10)}")
    print("Garden scores - Alice: 218")
    print(f"Total gardens managed: {GardenManager.get_total_gardens()}")

# 1.How do you organize complex systems with multiple interacting components?
#
# 分层设计，职责分离
# ┌─────────────────┐
# │   Presentation  │ ← 显示层（main函数，报告生成）
# ├─────────────────┤
# │     Service     │ ← 服务层（GardenManager，协调逻辑）
# ├─────────────────┤
# │     Domain      │ ← 领域层（Plant, FloweringPlant, PrizeFlower）
# ├─────────────────┤
# │   Utilities     │ ← 工具层（GardenStats，验证和统计）
# └─────────────────┘
# 2.What happens when you need different types of methods
# that belong to the class itself rather than individual instances?
# A: 当需要属于类本身而不是个别实例的不同类型方法时，我使用：
# 类方法 (@classmethod) - 操作类级别数据

# 3. 问这三个问题：
# "这个方法需要知道具体对象的信息吗？"
# 需要 → 实例方法（self）
# 不需要 → 继续问
# "这个方法需要知道类或所有对象的信息吗？"
# 需要 → 类方法（cls）
# 不需要 → 继续问
# "这个方法只是工具函数吗？"
# 是 → 静态方法（无参数）
