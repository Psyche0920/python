import functools
import operator


def spell_reducer(spells: list[int], operation: str) -> int:
    operations = {
        "add": operator.add,
        "multiply": operator.mul,
        "max": max,
        "min": min,
    }

    if operation not in operations:
        raise ValueError("Invalid operation")
    return functools.reduce(operations[operation], spells)


def partial_enchanter(base_enchantment: callable) -> dict[str, callable]:
    return {
        "fire_enchant": functools.partial(base_enchantment, 50, "fire"),
        "ice_enchant": functools.partial(base_enchantment, 50, "ice"),
        "lightning_enchant": functools.partial(base_enchantment, 50,
                                               "lightning")
    }


@functools.lru_cache(maxsize=None)
def memoized_fibonacci(n: int) -> int:
    if n < 2:
        return n
    return memoized_fibonacci(n - 1) + memoized_fibonacci(n - 2)


def spell_dispatcher() -> callable:
    @functools.singledispatch
    def dispatch(arg):
        return "Unknown spell type"

    @dispatch.register
    def _(arg: int) -> str:
        return f"Damage spell: {arg} power"

    @dispatch.register
    def _(arg: str) -> str:
        return f"Enchantment spell: {arg}"

    @dispatch.register
    def _(arg: list) -> str:
        return f"Multi-cast spell: {len(arg)} spells"

    return dispatch


def main() -> None:
    print()
    print("Testing spell reducer...")
    print("Sum:", spell_reducer([10, 20, 30, 40], "add"))
    print("Product:", spell_reducer([10, 20, 30, 40], "multiply"))
    print("Max:", spell_reducer([10, 20, 30, 40], "max"))
    print("Min:", spell_reducer([10, 20, 30, 40], "min"))
    print()

    def enchant(power: int, element: str, target: str) -> str:
        return f"{element} enchantment with {power} on {target}"
    enchants = partial_enchanter(enchant)
    print(enchants["fire_enchant"]("Sword"))  # "Sword" = target parameter
    print(enchants["ice_enchant"]("Shield"))
    print(enchants["lightning_enchant"]("Hammer"))
    print()

    print("Testing memoized fibonacci...")
    print("Fib(10):", memoized_fibonacci(10))
    print("Fib(15):", memoized_fibonacci(15))
    print()

    print("Testing spell dispatcher...")
    dispatcher = spell_dispatcher()
    print(dispatcher(50))
    print(dispatcher("Flaming Sword"))
    print(dispatcher(["fireball", "heal", "shield"]))


if __name__ == "__main__":
    main()

# Q1: How does functools.reduce enable powerful data aggregation?
# by repeatedly comb elements of an iterable into a single result using a func
# This makes it useful for operations like summation, multiplication,
# finding maximum or minimum values, and other cumulative transformations.
# Q2: What are the performance benefits of memoization with lru_cache?
# by storing the results of previous function calls and
# reusing them when the same inputs appear again.
# This avoids repeated computation,
# which is especially beneficial for recursive functions like Fibonacci,
# where many subproblems are calculated multiple times
#
# 1. functools.reduce(function, iterable)
# reduce(function, [a, b, c, d])====>function(function(function(a, b), c), d)
#
# 2. functools.partial
# 作用：
# 固定一部分参数，生成一个新函数
# def partial_enchanter(base_enchantment):

#     def fire_enchant(target):
#         return base_enchantment(50, "fire", target)

#     def ice_enchant(target):
#         return base_enchantment(50, "ice", target)

#     def lightning_enchant(target):
#         return base_enchantment(50, "lightning", target)

#     return {
#         "fire_enchant": fire_enchant,
#         "ice_enchant": ice_enchant,
#         "lightning_enchant": lightning_enchant
#     }
#
#
#  4. 为什么叫 single dispatch？
# 因为它只根据：
# 第一个参数的类型
# 来决定用哪个函数。
# 不是根据多个参数一起决定
# def dispatch(arg):
#     if isinstance(arg, int):
#         return f"Damage spell: {arg} power"
#     elif isinstance(arg, str):
#         return f"Enchantment spell: {arg}"
#     elif isinstance(arg, list):
#         return f"Multi-cast spell: {len(arg)} spells"
#     return "Unknown spell type"
