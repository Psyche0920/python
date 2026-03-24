from ex4.TournamentCard import TournamentCard
from ex4.TournamentPlatform import TournamentPlatform


def main() -> None:
    print()
    print("=== DataDeck Tournament Platform ===")
    print()
    print("Registering Tournament Cards...")
    print()

    platform = TournamentPlatform()
    dragon = TournamentCard(
        card_id="dragon_001",
        name="Fire Dragon",
        cost=5,
        rarity="Lengendary",
        attack_power=7,
        rating=1200,
    )
    wizard = TournamentCard(
        card_id="wizard_001",
        name="Ice Wizard",
        cost=4,
        rarity="Rare",
        attack_power=5,
        rating=1150,
    )

    platform.register_card(dragon)
    platform.register_card(wizard)

    for c in [dragon, wizard]:
        print(f"{c.name}(ID: {c.card_id}):")
        print("- Interfaces: [Card, Combatable, Rankable]")
        print(f"- Rating: {c.rating}")
        print(f"- Record: {c.wins}-{c.losses}")
        print()

    print("Creating tournament match...")
    match = platform.create_match("dragon_001", "wizard_001")
    print("Match Result:", match)
    print()

    print("Platform Report:")
    print(platform.generate_tournament_report())
    print()

    print("=== Tournament Platform Successfully Deployed! ===")
    print("All abstract patterns working together harmoniously!")


if __name__ == "__main__":
    main()

    #                     ┌──────────────────────┐
    #                     │   TournamentPlatform │
    #                     │       (ex4)          │
    #                     └──────────┬───────────┘
    #                                │
    #                     manages tournament
    #                                │
    #                 ┌──────────────┴──────────────┐
    #                 │                             │
    #           TournamentCard                GameEngine
    #              (ex4)                       (ex3)
    #                 │                             │
    #   ┌─────────────┼─────────────┐               │
    #   │             │             │               │
    #  Card       Combatable     Rankable          │
    #  (ex0)        (ex2)         (ex4)             │
    #   │                                          │
    #   │                                  ┌───────┴────────┐
    #   │                                  │                │
    #   │                             CardFactory       GameStrategy
    #   │                                (ex3)             (ex3)
    #   │                                  │                │
    #   │                         FantasyCardFactory  AggressiveStrategy
    #   │                                  │
    #   │                                  │
    #   └───────────── Deck (ex1) ─────────┘

# 1️⃣ How does multiple inheritance allow a class
# to implement several interfaces?
# 多重继承如何让一个类实现多个接口？
# 多重继承允许一个类同时继承多个父类。
# 每个父类提供不同的接口或能力。
# 子类需要实现所有父类要求的方法。
# 2️⃣ What are the benefits of combining ranking capabilities
# with card game mechanics?
# 将排名能力和卡牌机制结合有什么好处？
# 将排名能力和卡牌游戏机制结合，可以让系统更具有竞争性和结构性。
# 优点包括：
# 玩家或卡牌成长系统
# 根据比赛结果提升或降低评分。
# 锦标赛系统
# 卡牌可以参与正式比赛。
# 性能统计
# 胜负记录和评分可以衡量卡牌实力。
# 扩展游戏玩法
# 游戏从简单对战升级为完整的锦标赛平台。
# 3️⃣ 一句话总结（考试很好用）
# 多重继承使一个类能够组合多个接口，从而让卡牌同时具备游戏机制和锦标赛排名能力
