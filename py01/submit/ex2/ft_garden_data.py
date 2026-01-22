class Plant():
    def __init__(self, name: str, height_cm: int, age_days: int):
        self.name = name
        self.height_cm = height_cm
        self.age_days = age_days

    def grow(self):
        self.height_cm += 1

    def age_up(self):
        self.age_days += 1

    def get_info(self) -> str:
        return f"{self.name}: {self.height_cm}cm, {self.age_days} days old"


if __name__ == "__main__":
    plant1 = Plant("Rose", 25, 30)
    plant2 = Plant("Sunflower", 80, 45)
    print("=== Day 1 ===")
    print(plant1.get_info())
    print(plant2.get_info())
    print("=== Day 7 ===")
    for _ in range(6):
        plant1.grow()
        plant2.grow()
        plant1.age_up()
        plant2.age_up()
    print(plant1.get_info())
    print(plant2.get_info())
    print("Growth this week: +6cm per plant")

# 问：How are you handling the operations on plant data?
# 答：通过面向对象的方式，将数据操作封装在Plant类的方法中。每个植物对象管理自己的状态，通过grow()和age_up()方法修改内部数据。

# 问：Is there repetition in your code?
# 答：是的，存在重复。主要在对多株植物执行相同操作时，需要为每株植物单独调用方法。
# 以通过使用列表循环来消除这种重复。
