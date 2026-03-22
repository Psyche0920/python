def garden_operations():
    print("Testing ValueError...")
    try:
        int("abc")
    except ValueError:
        print("Caught ValueError: invalid literal for int()")

    print("\nTesting ZeroDivisionError...")
    try:
        10 / 0
    except ZeroDivisionError:
        print("Caught ZeroDivisionError: division by zero")

    print("\nTesting FileNotFoundError...")
    try:
        open("missing.txt", "r")
    except FileNotFoundError:
        print("Caught FileNotFoundError: No such file 'missing.txt'")

    print("\nTesting KeyError...")
    try:
        garden = {"tomato": 5}
        print(garden["lettuce"])
    except KeyError:
        print(r"Caught KeyError: 'missing\_plant'")


def test_error_types():
    print("=== Garden Error Types Demo ===\n")
    garden_operations()
    print("\nTesting multiple errors together...")
    try:
        int("abc")
        10 / 0
    except (ValueError, ZeroDivisionError):
        print("Caught an error, but program continues!")

    print("\nAll error types tested successfully!")


if __name__ == "__main__":
    test_error_types()

# BaseException
# ├── KeyboardInterrupt    (用户中断)
# ├── SystemExit           (系统退出)
# └── Exception
#     ├── ValueError       (值错误)
#     ├── TypeError        (类型错误)
#     ├── KeyError         (键错误)
#     ├── FileNotFoundError (文件未找到)
#     ├── ZeroDivisionError (除以零)
#     └── ... (还有很多)
#  你已经展示了两种捕获多种错误的方法：
# 方法A：每个错误类型单独处理（在 garden_operations() 中）
# 方法B：用元组一次捕获多种错误（在 test_error_types() 末尾）
# Q1: 为什么有不同的错误类型？
# 精确诊断：知道具体哪里出错了
# 针对处理：不同的错误需要不同的解决方案
# 代码清晰：提高可读性和可维护性
# 层次结构：反映问题的本质关系
# # Q2: 如何用一段代码捕获多种错误？"
# # 一个except用元组（你的写法）
# # 多个except分别写（另一个写法）
