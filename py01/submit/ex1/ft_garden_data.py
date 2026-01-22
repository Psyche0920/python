class Plant:
    def __init__(self, name: str, height_cm: int, age_days: int):
        self.name = name
        self.height_cm = height_cm
        self.age_days = age_days

    def display_info(self):
        print(f"{self.name}: {self.height_cm}cm, {self.age_days} days old")


if __name__ == "__main__":
    print("=== Garden Plant Registry ===")
    plant1 = Plant("Rose", 25, 30)
    plant2 = Plant("Sunflower", 80, 45)
    plant3 = Plant("Cactus", 15, 120)
    plant1.display_info()
    plant2.display_info()
    plant3.display_info()

# 你的理解完全正确：self 是占位符（形参），真正的数据（实参 plant1)
# 我目前使用一个 Plant 类来存储植物信息。每一株植物都是 Plant 类的一个实例，对象中保存属性。
# 具体的植物对象在 main() 函数中创建，并通过类的方法来显示它们的信息。
