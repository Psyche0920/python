def ft_seed_inventory(seed_type: str, quantity: int, unit: str) -> None:
    name = seed_type.capitalize()

    if unit == "packets":
        print(f"{name} seeds: {quantity} packets available")
    elif unit == "grams":
        print(f"{name} seeds: {quantity} grams total")
    elif unit == "area":
        print(f"{name} seeds: covers {quantity} square meters")
    else:
        print("Unknown unit type")

# .capitalize()：首字母大写，其余小写
# .title()：每个单词首字母大写
# -> None: 表示这个函数不返回任何值，它只执行打印操作。
# def add(a: int, b: int) -> int:  # -> int 表示返回整数
# 在Python中，如果函数没有 return 语句，或者只有 return 没有值，它默认返回 None
# 即使不写，函数也返回 None，但写了更清晰练习7要求类型注解，所以必须写
# 类型提示只是"提示"，Python 运行时完全忽略它们。即使传入错误的类型，程序也会正常运行（除非代码本身因为类型错误而崩溃）。
# f"{}"：f-string，现代Python的字符串格式化方法，简洁高效
# print(name + " seeds: " + str(quantity) + " packets available")
