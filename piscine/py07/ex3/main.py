from ex3.FantasyCardFactory import FantasyCardFactory
from ex3.AggressiveStrategy import AggressiveStrategy
from ex3.GameEngine import GameEngine


def format_hand(hand: list) -> str:
    """
    Convert a list of card objects into a formatted string representation.

    Each card is displayed using the format:
        CardName (Cost)

    Example:
        [Fire Dragon (5), Goblin Warrior (2), Lightning Bolt (3)]

    Args:
        hand (list):
            A list of card objects that contain 'name' and 'cost' attributes.

    Returns:
        str:
            A formatted string representing the cards currently in the hand.
    """

    parts = [f"{c.name} ({c.cost})" for c in hand]
    return "[" + ", ".join(parts) + "]"


def main() -> None:
    """
    Entry point for the DataDeck game engine demonstration.

    This function performs the following steps:

    1. Initializes the fantasy card factory.
    2. Selects an aggressive gameplay strategy.
    3. Configures the game engine with the chosen factory and strategy.
    4. Displays the available card types supported by the factory.
    5. Simulates one game turn using the strategy.
    6. Prints a summary of the turn execution and game statistics.

    This demonstration showcases the interaction between:
        - Abstract Factory Pattern (card creation)
        - Strategy Pattern (gameplay decision logic)
        - GameEngine (system orchestration)
    """
    print()
    print("=== DataDeck Game Engine ===")
    print()
    print("Configuring Fantasy Card Game.")

    factory = FantasyCardFactory()
    strategy = AggressiveStrategy()
    engine = GameEngine()
    engine.configure_engine(factory, strategy)

    print("Factory:", factory.__class__.__name__)
    print("Strategy", strategy.get_strategy_name())
    print("Available types:", factory.get_supported_types())
    print()

    print("Simulating aggressive turn.")
    print("Hand:", format_hand(engine.hand))
    print()

    turn = engine.simulate_turn()
    print("Turn execution:")
    print("Strategy:", turn["strategy"])
    print("Actions:", turn["actions"])
    print()

    print("Game Report:")
    print(engine.get_engine_status())
    print()

    print("Abstract Factory + Strategy Pattern: Maximum flexibility achieved!")


if __name__ == "__main__":
    main()


# 1. ",".join(parts) 是什么？
# join() 是字符串方法。
# 作用：
# 用某个字符把列表里的字符串连接起来
# 2. print("Factory:", factory.__class__.__name__)
# print("Strategy:", strategy.get_strategy_name())
# 完全没问题，因为：
# Factory 没有 name method
# Strategy 有 name method

# 1️⃣ How do Abstract Factory and Strategy patterns work together?
# 抽象工厂和策略模式如何一起工作？
# English
# work together by separating object creation from gameplay behavior.
# Abstract Factory creates game objects e.g.cards, creatures, spells & decks.
# Strategy decides how the game actions are performed,
# e.g. which cards to play & which targets to attack.
# The GameEngine connects them:
# it uses the factory to generate cards and uses the strategy to execute a turn
# This allows the engine to
# remain independent from specific card types and gameplay logic.
# 中文
# 抽象工厂（Abstract Factory）和策略模式（Strategy）通过把 对象创建 和 游戏行为逻辑 分离来协同工作。
# 抽象工厂负责创建游戏对象，例如卡牌、生物、法术和牌组。
# 策略模式负责决定游戏如何执行行动，例如打出哪些卡牌、攻击哪些目标。
# GameEngine 负责连接两者：
# 它使用工厂生成卡牌，并使用策略来执行游戏回合。
# 这样引擎本身不需要依赖具体卡牌类型或具体玩法逻辑。

# 2️⃣ What makes this combination powerful for game engine systems?
# 为什么这种组合在游戏引擎中很强大？
# English
#  it provides flexibility, modularity, and extensibility.
# Flexibility
# You can change the card theme by switching factories (e.g. Fantasy → Sci-Fi).
# Modularity
# Card creation and gameplay logic are implemented in separate components.
# Extensibility
# New factories or strategies can be added without modifying the game engine.
# Low coupling
# The engine does not depend on specific card implementations orgameplay rules.
# 中文
# 这种组合强大的原因在于它提供了 灵活性、模块化和可扩展性。
# 灵活性（Flexibility）
# 只需更换工厂，就可以改变游戏主题，例如从 Fantasy 改为 Sci-Fi。
# 模块化（Modularity）
# 卡牌创建逻辑和游戏策略逻辑被分成不同模块。
# 可扩展性（Extensibility）
# 可以轻松添加新的工厂或新的策略，而无需修改游戏引擎。
# 低耦合（Low coupling）
# 引擎不依赖具体卡牌实现或具体游戏规则。
