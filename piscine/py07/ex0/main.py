from ex0.CreatureCard import CreatureCard
# from ex0.Card import Card


def main() -> None:
    print()
    print("=== DataDeck Card Foundation ===")
    print()
    print("Testing Abstract Base Class Design:")
    print()

    dragon = CreatureCard(name="Fire Dragon", cost=5,  # Card
                          rarity="Legendary", attack=7, health=5)
    print("CreatureCard Info:")
    print(dragon.get_card_info())
    print()

    available_mana = 6
    print(f"Playing {dragon.name} with {available_mana} mana available:")
    print("Playable:", dragon.is_playable(available_mana))
    print("Play result:", dragon.play(game_state={"mana": available_mana}))
    print()

    print(f"{dragon.name} attacks Goblin Warrior:")
    print("Attack result:", dragon.attack_target("Goblin Warrior"))
    print()

    low_mana = 3
    print(f"Testing insufficient mana ({low_mana} available)")
    print("Playable:", dragon. is_playable(low_mana))
    print()

    print("Abstract pattern successfully demonstrated!")


if __name__ == "__main__":
    main()

# 抽象基类（Abstract Base Class, ABC）能保证不同卡牌类型的一致性，核心靠两件事：
# 统一合同（contract） + 强制检查（enforcement）。
# 1) 抽象基类如何确保不同卡牌类型的一致性？
# a. 统一合同
#  Card(ABC) 里规定“所有卡牌都必须具备的行为”，比如：
# 必须能 play(game_state)（打出产生效果）
# 并且共享基础属性与通用方法（如 name/cost/rarity，get_card_info()，is_playable()）
# 这样无论是 CreatureCard、以后你写的 SpellCard、ArtifactCard，都必须满足同样的接口形状：
# 游戏引擎/Deck 只需要调用 card.play(...)，不需要关心具体是哪种卡
# 这就实现了多态（polymorphism）：同一个接口，不同实现
# b. 强制一致（不是约定，是强制）
# @abstractmethod 把 play 变成“必须完成的任务”。
# 如果某个子类没实现 play，它就仍然是“抽象的”，不能被创建对象，这会逼着你按规则来。
#
# 2) 如果你直接创建 Card 会发生什么？
# 如果你写：
# c = Card("X", 1, "Common")
# 会立刻报错（TypeError）：
# 大意是：不能实例化抽象类 Card，因为它还有抽象方法 play 没实现
# 原因是：Card 本身只定义了接口（合同），没有给出 play 的具体行为；Python 的 ABC 机制
# 会在实例化时检查是否仍有未实现的抽象方法，若有就禁止创建对象。
