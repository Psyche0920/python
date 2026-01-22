def check_plant_health(plant_name, water_level, sunlight_hours):
    if not plant_name:
        raise ValueError("Error: Plant name cannot be empty!")
    if water_level > 10:
        raise ValueError(f"Error: Water level {water_level} "
                         f"is too high (max 10)")
    if water_level < 1:
        raise ValueError(f"Error: Water level {water_level} "
                         f"is too low (min 1)")
    if sunlight_hours > 12:
        raise ValueError(f"Error: Sunlight hours {sunlight_hours} "
                         f"is too high (max 12)")
    if sunlight_hours < 2:
        raise ValueError(f"Error: Sunlight hours {sunlight_hours} "
                         f"is too low (min 2)")
    print(f"Plant '{plant_name}' is healthy!")


def test_plant_checks():
    print("=== Garden Plant Health Checker ===\n")
    print("Testing good values...")
    try:
        check_plant_health("tomato", 7, 8)
    except ValueError as e:
        print(e)

    print("\nTesting empty plant name...")
    try:
        check_plant_health("", 7, 8)
    except ValueError as e:
        print(e)
    print("\nTesting bad water level...")
    try:
        check_plant_health("tomato", 15, 8)
    except ValueError as e:
        print(e)

    print("\nTesting bad sunlight hours...")
    try:
        check_plant_health("tomato", 7, 0)
    except ValueError as e:
        print(e)

    print("\nAll error raising tests completed!")


if __name__ == "__main__":
    test_plant_checks()

# Q2: if not x: vs if x is None:
# [plant_name is None] checks only for None,
# [if not plant_name] checks for all falsy values
# such as None and empty strings, which better matches the business rule.
# 在 Python 里，以下值都是 False：
# None
# ""
# []
# {}
# 所以它能拦住：
# 空名字
# 没有名字
# 非常适合“不能为空”的业务语义
# Q3:
# 在你这种“只要有一个条件出错就抛异常”的函数里：
# 把所有检查写成 if ...: raise ...，最后直接写 print(...)，不用 else，一般更清晰。
# 如果写 if/elif/.../else，也可以，但要保证结构干净、条件互斥，用来表达逻辑分类，而不是只给最后一个 if 配一个 else。
#
# 1. 什么时候应该 raise？
# 在你的代码中，应该 raise 当：
# 输入数据明显错误（如空名称）
# 数值超出安全范围（水量1-10，光照2-12）
# 继续执行会有风险（无效数据会导致错误结果）
#
# 2. 如何创建有用的错误信息？
# 你的代码已经做到了：
# 具体指出问题："Water level 15 is too high"
# 包含实际值：15
# 提供期望值：(max 10)
