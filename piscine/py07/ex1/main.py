from ex0.CreatureCard import CreatureCard
from ex1.SpellCard import SpellCard
from ex1.ArtifactCard import ArtifactCard
from ex1.Deck import Deck


def main() -> None:
    print()
    print("=== DataDeck Deck Builder ===")
    print()
    print("Building deck with different card types...")

    deck = Deck()
    deck.add_card(SpellCard("Lightning Bolt", 3, "Common", "damage"))
    deck.add_card(CreatureCard("Fire Dragon", 5, "Legendary", 7, 5))
    deck.add_card(ArtifactCard("Mana Crystal", 2, "Rare",
                               durability=3, effect="+1 mana per turn"))

    print("Deck stats:", deck.get_deck_stats())
    print()

    deck.shuffle()
    print("Drawing and playing cards:")
    print()

    while True:
        try:
            card = deck.draw_card()
        except IndexError:
            break

        info = card.get_card_info()
        print(f"Drew: {card.name} ({info.get('type', 'Card')})")
        print("Play result:", card.play(game_state={"mana": 10}))
        print()

    print("Polymorhism in action: Same interface, different behaviors!")


if __name__ == "__main__":
    main()

# Deck = 牌组
# Builder = 构建者
# Mana = 魔法值 / 法力值
# “Artifact card” 通常出现在**卡牌游戏（card game）**里，意思是：神器牌 / 道具牌
# # 在 main 里临时加：
# print(deck.remove_card("Lightning Bolt"))
# # 把 while 循环跑完后再加：
# # deck.draw_card()  # 应该抛 IndexError
#
# Q1: How does polymorphism enable the Deck to work with any card type?
# All cards inherit from Card.
# All cards have a play() method.
# Deck only works with Card.
# Deck does not care about the real type.
# When Deck calls card.play(), Python chooses the correct version.
# This is called polymorphism.
# Example:
# card.play(game_state)
# If the card is:
# Spell → Spell’s play() runs.
# Creature → Creature’s play() runs.
# Artifact → Artifact’s play() runs.
# Deck does not need if statements.

# Q2: What are the benefits of this design pattern for card game systems?
# ✅ 1. Easy to add new cards
# You can create:
# class TrapCard(Card):
# You do not change Deck.
# Deck still works.
# ✅ 2. Cleaner code
# No need to write:
# if isinstance(card, SpellCard):
# Code is shorter and cleaner.
# ✅ 3. Flexible system
# You can mix many card types in one deck.
# Deck treats them the same way.
# ✅ 4. Easy to maintain
# If you change SpellCard logic,
# you do not touch Deck.
