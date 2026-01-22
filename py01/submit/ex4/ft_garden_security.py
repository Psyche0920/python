class SecurePlant:
    def __init__(self, name):
        self._name = name
        self._height = 0
        self._age = 0

    def get_name(self):
        return self._name

    def get_height(self):
        return self._height

    def get_age(self):
        return self._age

    def set_height(self, height):
        if height < 0:
            print(f"Invalid operation attempted: height {height}cm [REJECTED]")
            print("Security: Negative height rejected")
        else:
            self._height = height
            print(f"Height updated: {height}cm [OK]")

    def set_age(self, age):
        if age < 0:
            print(f"Invalid operation attempted: age {age} days [REJECTED]")
            print("Security: Negative age rejected")
        else:
            self._age = age
            print(f"Age updated: {age} days [OK]")

    def get_info(self):
        return f"{self._name} ({self._height}cm, {self._age} days)"


if __name__ == "__main__":
    print("== Garden Security System ==")
    plant = SecurePlant("Rose")
    print(f"Plant created: {plant.get_name()}")
    plant.set_height(25)
    plant.set_age(30)
    print()
    plant.set_height(-5)
    print()
    print(f"Current plant: {plant.get_info()}")

# Q: How can you protect your data from being accidentally corrupted?
# A: 我通过封装(encapsulation)和数据验证(data validation)来保护数据不被意外破坏：
#
# 1. 使用私有属性（命名约定）
# python
# class SecurePlant:
#     def __init__(self, name):
#         self._name = name      # 使用下划线前缀表示"受保护"
#         self._height = 0       # 外部不应该直接访问
#         self._age = 0          # 只能通过getter/setter访问
# 2. 提供受控的访问方法
# python
#     # Getter方法 - 只读访问
#     def get_height(self):
#         return self._height
#
#     # Setter方法 - 带验证的写访问
#     def set_height(self, height):
#         if height < 0:                    # 验证逻辑
#             print("Security: Negative height rejected")
#             return False                  # 拒绝无效数据
#         self._height = height             # 只存储有效数据
#         return True
# 3. 数据验证机制
# python
#     def set_age(self, age):
#         if age < 0:                       # 检查年龄是否为负
#             print(f"Invalid operation attempted: age {age} days [REJECTED]")
#             print("Security: Negative age rejected")
#             return False                  # 防止数据损坏
#         self._age = age                   # 只有有效数据才存储
#         return True
