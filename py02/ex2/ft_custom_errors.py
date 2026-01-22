class GardenError(Exception):
    def __init__(self, message):
        super().__init__(message)


class PlantError(GardenError):
    def __init__(self, message):
        super().__init__(message)


class WaterError(GardenError):
    def __init__(self, message):
        super().__init__(message)


def test_custom_errors():
    print("=== Custom Garden Errors Demo ===\n")
    print("Testing PlantError...")
    try:
        raise PlantError("The tomato plant is wilting!")
    except PlantError as e:
        print(f"Caught PlantError: {e}")

    print("\nTesting WaterError...")
    try:
        raise WaterError("Not enough water in the tank!")
    except WaterError as e:
        print(f"Caght WaterError: {e}")
    print("\nTesting catching all garden errors...")
    try:
        raise PlantError("The tomato plant is wilting!")
    except GardenError as e:
        print(f"Caught a garden error: {e}")

    try:
        raise WaterError("Not enough water in the tank!")
    except GardenError as e:
        print(f"Caught a garden error: {e}")
    print("\nAll custom error types work correctly!")


if __name__ == "__main__":
    test_custom_errors()

# Q1：为什么不直接用 ValueError？
# ValueError 无法表达业务语义，自定义异常能让错误更清晰，也更容易维护大型系统。
# Q2：继承异常有什么好处？
# 通过继承，可以统一捕获同一类业务错误，同时保留对具体错误的精细控制。
# Q3：什么时候该用自定义异常？
# 👉 记住一句话就够：
# 当错误和“业务逻辑”强相关时，就该用。
# 继承如何帮助组织错误？
# 层次清晰：创建逻辑分明的错误分类
# 灵活处理：可以精确处理或统一处理相关错误
# 代码复用：公共功能在基类中定义，子类继承
# 易于扩展：添加新错误类型时保持结构一致性
# 维护简单：相关错误组织在一起，便于管理和理解
# 最佳实践：像组织文件系统一样组织你的异常类——创建有意义的目录（父类）和文件（子类），使整个系统结构清晰、易于导航和维护。
# #
# Q4: Python 的错误世界是“类体系”
# 在 Python 里，错误不是字符串，也不是状态码，而是——
# 👉 对象（object）
# 而这些对象，全都是类（class）实例。
# 大致结构是这样的（简化版）：
# BaseException
#  └── Exception
#       ├── ValueError
#       ├── TypeError
#       ├── KeyError
#       ├── FileNotFoundError
#       └── ...
# Q5: Python 只允许 继承自 BaseException 的类 被 raise。
# We use [raise] to actively signal illegal states and
#  transfer error handling responsibility to higher-level logic,
# instead of silently continuing in a corrupted state.
#
# Q6: We use [super()] when overriding __init__ to ensure
# the parent exception is properly initialized,
# because inheritance alone does not automatically
# execute the parent constructor.
#
# Q7:The exception instance always exists,
# but it is only accessible when we bind it using as e.
#
#
# 就像数学：
# 所有正方形都是矩形（继承关系）
# 但正方形有自己特殊的属性（边长相等）
# class 矩形:
#     def __init__(self, 长, 宽):
#         self.长 = 长
#         self.宽 = 宽
# class 正方形(矩形):  # 正方形继承矩形
#     def __init__(self, 边长):
#         super().__init__(边长, 边长)  # 长=宽=边长
#         self.边长 = 边长
# 创建一个正方形
# 我的图形 = 正方形(5)  # 这是一个正方形对象
# 问：我的图形是矩形吗？是的！（因为继承）
# 问：我的图形的长和宽是多少？都是5（这是正方形对象自己的属性）
# 问：可以说"处理所有矩形"来处理这个正方形吗？是的！
# 异常也是一样：
# PlantError对象 是 GardenError，但有自己特定的消息
