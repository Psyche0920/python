def spell_combiner(spell1: callable, spell2: callable) -> callable:
    # callable as type: function-like object
    # callable() as function：check if it's a function
    def combined(*args, **kwargs):
        return (spell1(*args, **kwargs), spell2(*args, **kwargs))
    return combined


def power_amplifier(base_spell: callable, multiplier: int) -> callable:
    def amplified(*args, **kwargs):
        return base_spell(*args, **kwargs) * multiplier
    return amplified


def conditional_caster(condition: callable, spell: callable) -> callable:
    def caster(*args, **kwargs):
        if condition(*args, **kwargs):
            return spell(*args, **kwargs)
        return "Spell fizzled"
    return caster


def spell_sequence(spells: list[callable]) -> callable:
    def sequence(*args, **kwargs):
        results = []
        for spell in spells:
            results.append(spell(*args, **kwargs))
        return results
    return sequence


def main() -> None:
    def fireball(target: str) -> str:
        return f"Fireball hits {target}"

    def heal(target: str) -> str:
        return f"Heals {target}"

    def damage(target: str) -> int:
        if target == "Dragon":
            return 10
        return 5

    def strong_enough(target: str) -> bool:
        return target == "Dragon"

    print()
    print("Testing spell combiner...")
    combined = spell_combiner(fireball, heal)  # only execute outlayer
    print(combined("Dragon"))  # execute innerlayer
    print()

    print("Testing power amplifier...")
    mega_damage = power_amplifier(damage, 3)
    print("Original:", damage("Dragon"))
    print("Amplified:", mega_damage("Dragon"))
    print()

    print("Testing conditional caster...")
    safe_cast = conditional_caster(strong_enough, fireball)
    print(safe_cast("Dragon"))
    print(safe_cast("Goblin"))
    print()

    print("Testing spell sequence...")
    seq = spell_sequence([fireball, heal])
    print(seq("Knight"))
    print()


if __name__ == "__main__":
    main()

# Q1. higher-order function
# 高阶函数: 函数处理函数:
# 函数可以接收另一个函数
# 函数可以返回一个新函数
# reuse and composition:
# function + function → new function
#
# Q2. 什么是 “first-class citizens”
# 在编程语言里，如果一个东西是 first-class citizen（第一类对象），意味着它可以：
# 1️⃣ 被赋值给变量
# 2️⃣ 作为函数参数传递
# 3️⃣ 作为函数返回值
# 4️⃣ 存储在数据结构中（list / dict 等）
#
# 3. *args:
# 接收任意数量的[位置参数]
# *args = 把很多位置参数打包成一个 tuple。
# combined("Dragon")
# args == ("Dragon",)
# combined("Dragon", 10)
# args == ("Dragon", 10)
#
# **kwargs:
# 接收任意数量的[关键字参数]
# **kwargs = 把很多 key=value 参数打包成一个 dict。
# combined(target="Dragon", power=10)
# kwargs == {"target": "Dragon", "power": 10}
#
# 4. [callable]
# means an object that can be called like a function using parentheses ().
# 中文
# 就是可以像函数一样用 () 调用的对象
#
