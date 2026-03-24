def mage_counter() -> callable:
    count = 0

    def counter() -> int:
        nonlocal count
        count += 1
        return count
    return counter


def spell_accumulator(initial_power: int) -> callable:
    total_power = initial_power

    def accumulator(amount: int) -> int:
        nonlocal total_power
        total_power += amount
        return total_power
    return accumulator


def enchantment_factory(enchantment_type: str) -> callable:
    def enchant(item_name: str) -> str:
        return f"{enchantment_type} {item_name}"
    return enchant


def memory_vault() -> dict[str, callable]:
    storage = {}

    def store(key: str, value):
        storage[key] = value

    def recall(key: str):
        return storage.get(key, "Memory not found")

    return {
        "store": store,
        "recall": recall
    }


def main() -> None:
    print()
    print("Testing mage counter...")
    counter = mage_counter()
    print("Call 1:", counter())
    print("Call 2:", counter())
    print("Call 3:", counter())
    print()

    print("Testing spell accumulator...")
    acc = spell_accumulator(10)
    print(acc(5))
    print(acc(15))
    print(acc(20))
    print()

    print("Testing enchantment factory...")
    flaming = enchantment_factory("Flaming")
    frozen = enchantment_factory("Frozen")
    print(flaming("Sword"))
    print(frozen("Shield"))
    print()

    print("Testing memory vault...")
    vault = memory_vault()
    vault["store"]("artifact", "Crystal Orb")
    vault["store"]("spell", "Fireball")
    print(vault["recall"]("artifact"))
    print(vault["recall"]("unknown"))
    print()


if __name__ == "__main__":
    main()


# 1️⃣ How do closures enable functions to "remember" their creation environment
# Closures allow a function to remember variables from its enclosing scope
# even after the outer function has finished executing.
# The inner function keeps a reference to those variables,
# so it can access and use them later.
# 2️⃣ What are the benefits of lexical scoping in functional programming?
# Lexical scoping allows functions to access variables from the environment
# in which they were defined.
# This enables closures, improves modularity, and allows functions to
# maintain private state without using global variables.
# Lexical scoping 是规则（rule）, 词法作用域表示：函数会在它定义时所在的作用域中查找变量，包括外层函数的作用域。
# Closure 是结果（result / mechanism）, losure 是一个函数，它携带了它定义时的环境变量。
#
# closure = inner function + remembered outer variables
# 闭包 = 内部函数 + 记住的外部变量
#
# global 是去找函数外的全局变量
# nonlocal 是去找外层函数的变量
#
# 3. 函数	原因
# mage_counter	需要 nonlocal count，因为修改变量
# spell_accumulator	需要 nonlocal total_power
# enchantment_factory	不需要，因为[只读取变量]
# memory_vault	不需要，因为[修改 dict 内容]
#
# 4. count 不是 global，它是 外层函数的局部变量，被 inner function 通过 closure 记住了。
# spell_accumulator 会一直在上一次的结果上继续加，不会每次回到初始值。
#
# enchantment_type 每次不同，如果把它变成 nonlocal 会不会 persist？
# 不需要 nonlocal
# 原因是：没有修改 enchantment_type, everytime new execution
# 在 Python 中：
# 读取外层变量 → 不需要 nonlocal
# 修改外层变量 → 必须 nonlocal
#
# 5. [mutable object]
# dict itself has this nature already
# 这是 Python 里一个重要概念：
# dict / list / set 都是：
# mutable
# # 所以可以修改内容而不重新绑定变量。
#
# 情况 1：修改 dict 内容
# storage ──► {}
# storage["a"] = 1
# storage ──► {"a":1}
# storage → 还是原来的 dict
# 变量 storage 没有改变指向。
# 所以 Python 认为：你只是修改对象内容, 因此不需要 nonlocal。
#
# 情况 2：改变变量本身
# storage ──► {}
# storage = {"a":1}
# storage ──► {"a":1}
# 变量 storage 被重新绑定
# 如果在 inner function 里这么做：
# def inner():
#     storage = {"a":1}
# Python会认为：storage 是 inner 的局部变量, 如果你想修改外层变量，就必须：nonlocal storage
