class Plant:
    def __init__(self, name, height, age):
        self.name = name
        self.height = height
        self.age = age

    def info(self):
        return f"{self.name} ({self.height}cm, {self.age} days)"


if __name__ == "__main__":
    plants = [
        Plant("Rose", 25, 30),
        Plant("Oak", 200, 365),
        Plant("Cactus", 5, 90),
        Plant("Sunflower", 80, 45),
        Plant("Fern", 15, 120)
    ]

    print("=== Plant Factory Output ===")
    for p in plants:
        print("Created:", p.info())

    print(f"\nTotal plants created: {len(plants)}")

# ft_plant_factory.py
#
# class Plant:
#     def __init__(self, name: str, height_cm: int, age_days: int):
#         self.name = name
#         self.height_cm = height_cm
#         self.age_days = age_days
#
#     def info(self):
#         return f"{self.name} ({self.height_cm}cm, {self.age_days} days)"
#
#
# def main():
#     # 植物数据列表
#     plant_data = [
#         ("Rose", 25, 30),
#         ("Sunflower", 80, 45),
#         ("Cactus", 15, 120),
#         ("Oak", 200, 365),
#         ("Fern", 15, 120)
#     ]
#
#     # 使用[列表]推导式批量创建（最简洁）: [expression for item in iterable if condition]
#     plants = [Plant(name, height, age) for name, height, age in plant_data]
#
#     print("=== Plant Factory Output ===")
#     for plant in plants:
#         print(f"Created: {plant.info()}")
#
#     print(f"\nTotal plants created: {len(plants)}")
#
#
# if __name__ == "__main__":
#     main()
# 方法1	              方法2
# 直接存储Plant对象	先存储元组，再转换为Plant对象(列表推导式)

# "Each plant should be ready to use immediately after construction" 这句话的意思是：
# 每个植物对象在创建（构造）完成后就应该立即可以使用。
# 这意味着：
# 构造函数 (__init__) 应该完成所有必要的初始化工作
# 对象创建后不需要额外的设置步骤
# 所有属性都应该在构造时被正确赋值
# 对象的状态是完整的，可以立即调用其方法
