import functools
import time


def spell_timer(func: callable) -> callable:
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Casting {func.__name__}...")
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"Spell completed in {end - start:.3f} seconds")
        return result
    return wrapper


def power_validator(min_power: int) -> callable:
    def decorator(func: callable) -> callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            power = args[-1]
            if power < min_power:
                return "Insufficient power for this spell"
            return func(*args, **kwargs)
        return wrapper
    return decorator


def retry_spell(max_attempts: int) -> callable:
    def decorator(func: callable) -> callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 1
            while attempt <= max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception:
                    if attempt == max_attempts:
                        return (f"Spell casting failed "
                                f"after {max_attempts} attempts")
                    print(f"Spell failed, retrying... (attempt"
                          f"{attempt}/{max_attempts})")
                    attempt += 1
        return wrapper
    return decorator


class MageGuild:
    @staticmethod
    def validate_mage_name(name: str) -> bool:
        return (
            len(name) >= 3
            and all(c.isalpha() or c == " " for c in name)
            and any(c.isalpha() for c in name)
        )

    @power_validator(10)
    # cast_spell = power_validator(10)(cast_spell)
    def cast_spell(self, spell_name: str, power: int) -> str:
        return f"Successfully cast {spell_name} with power {power}"


def main() -> None:
    print()
    print("Testing spell timer...")

    @spell_timer
    def fireball() -> str:
        time.sleep(0.1)
        return "Fireball cast!"
        # fireball = spell_timer(fireball)
    print("Result:", fireball())

    print()
    print("Testing MageGuild...")
    print(MageGuild.validate_mage_name("Gandalf"))
    print(MageGuild.validate_mage_name("A1"))

    guild = MageGuild()
    print(guild.cast_spell("Lightning", 15))
    print(guild.cast_spell("Ice", 5))

    print()
    print("Testing retry spell failure...")

    @retry_spell(3)
    def broken_spell() -> str:
        raise ValueError("Spell failed")
    # retry_spell(3)(broken_spell)
    print(broken_spell())

    print()
    print("Testing retry spell success...")


if __name__ == "__main__":
    main()


# Q1. [Decorators]
# Decorators separate additional behavior from the core logic of a function,
# improving code reuse and maintainability.
# def cast_spell(power):
#     start = time.time()

#     if power < 10:
#         return "Insufficient power"

#     result = "Spell cast!"

#     end = time.time()
#     print(end - start)

    # return result
#
# @spell_timer
# @power_validator(10)
# def cast_spell(power):
#     return "Spell cast!"

# Q2. [staticmethod]
# A static method belongs to a class but does not operate on an instance,
# while an instance method requires self and interacts with object data.

#  1. [function decrators]
# @func1
# @func2
# def func3
# 为什么等于：
# func3 = func1(func2(func3))
# 答案是：
# Python 会 从下往上应用 decorator
#
#     Python 实际执行的是：
# fireball = spell_timer(spell_counter(fireball))
# 执行顺序：
# spell_counter
# ↓
# spell_timer
# ↓
# fireball
#
# def deco1(f):
#     def wrapper():
#         print("deco1 start")
#         f()
#         # def wrapper():
#         # print("deco2 start")
#         # f()
#         # # def hello():
#         #     # print("hello")
#         # print("deco2 end")
#         print("deco1 end")
#     return wrapper
#
# def deco2(f):
#     def wrapper():
#         print("deco2 start")
#         f()
#         # def hello():
#             # print("hello")
#         print("deco2 end")
#     return wrapper
#
# @deco1
# @deco2
# def hello():
#     print("hello")
#
# hello=deco1(deco2(hello))
#
# 2. [args, kwargs]
# Python 是根据调用方式来决定它属于 args (without name) 还是 kwargs(with name)。
# pell("dragon", power=50)
# 结果：
# args = ("dragon",)
# kwargs = {"power": 50}

# 3.  @functools.wraps(func)
# # copy the meta info of func into wrapper
# wrapper.__name__ = func.__name__
# wrapper.__doc__ = func.__doc__
# wrapper.__annotations__ = func.__annotations__
# wrapper 的作用是在 func 前后加逻辑


# 4. decorator with or without parameters
# power_validator(10)
#         ↓
#     decorator
#         ↓
# decorator(cast_spell)
#         ↓
# wrapper
# @decorator
# def f():
# ||
# f = decorator(f)

# @decorator(x)
# def f():
# ||
# f = decorator(x)(f)

# 5. inner function reads outer variable
# 你只是读取 min_power，没有修改它。
# Python 规则是：
# 读取外层变量：不需要 nonlocal
# 修改外层变量：需要 nonlocal
# 这里 min_power 是被 closure 记住的。

# 6. staticmethod
# 没有 self
# 不需要实例
# 可以直接通过类调用
