from ex2.EliteCard import EliteCard


def main() -> None:
    print()
    print("=== DataDeck Ability System ===")
    print()

    elite = EliteCard(name="Arcane Warrior", cost=5,
                      rarity="Legendary", mana=8)

    print("EliteCard capabilities:")
    print("- Card:", ["play", "get_card_info", "is_playable"])
    print("- Combatable:", ["attack", "defend", "get_combat_stats"])
    print("- Magical:", ["cast_spell", "channel_mana", "get_magic_stats"])
    print()

    print(f"Playing {elite.name} (Elite Card):")
    print()
    print("Combat phase:")
    print("Attack result:", elite.attack("Enemy"))
    print("Defense result:", elite.defend(5))
    print()

    print("Magic phase:")
    print("Spell cast:", elite.cast_spell("Fireball", ["Enemy1", "Enemy2"]))
    print("Mana channel:", elite.channel_mana(3))
    print()

    print("Multiple interface implementation successful!")


if __name__ == "__main__":
    main()


# Q1:How do multiple interfaces enable flexible card design?
# Multiple interfaces make card design flexible
# because they separate abilities into independent parts.
# Each interface represents one type of ability.
# A card can implement one interface or several.
# The system interacts with abilities, not concrete classes.
# You can add new card types without changing existing engine logic.

# Example:
# A creature card → implements Combatable
# A spell card → implements Magical
# An elite card → implements both Combatable and Magical
# This means behavior is based on capability, not class name.

# Q2: What are the advantages of separating combat and magic concerns?
# 更清晰：战斗方法只放在战斗接口里，魔法方法只放在魔法接口里。
# 更少无用方法：法术卡不用被迫实现 attack()，生物卡不用被迫实现 cast_spell()。
# 更容易扩展：你可以加新接口（比如 Stealthable、Healable），不影响旧代码。
# 更容易维护：改战斗系统不会影响魔法系统，改魔法也不会影响战斗。
# 更少 if/elif：系统只检查“是否实现接口”，不用判断具体是哪种卡。
# 一句话总结：
# 多接口 = 能力拼装；分离关注点 = 代码干净、可扩展、好维护。
