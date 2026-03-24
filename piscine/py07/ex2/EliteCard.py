from enum import Enum
from ex0.Card import Card
from ex2.Combatable import Combatable
from ex2.Magical import Magical


class CombatType(Enum):
    MELEE = "melee"
    MAGIC = "magic"
# use enum to prevent silent bug = raise Error


class EliteCard(Card, Combatable, Magical):
    # Represents powerful cards with multiple abilities
    """EliteCard: multiple inheritance (Card + Combatable + Magical)."""
    def __init__(self, name: str, cost: int, rarity: str,
                 attack: int = 5, health: int = 5,
                 mana: int = 4, spell_power: int = 4):
        # but in magaical and combatable they didnt inititate the values???

        super().__init__(name, cost, rarity)
        # what if name and cost comes from different parent classes>

        if not isinstance(attack, int) or attack <= 0:
            raise ValueError("attack must be a positive int")
        if not isinstance(health, int) or health <= 0:
            raise ValueError("health must be a postive int")
        if not isinstance(mana, int) or mana < 0:
            raise ValueError("mana must be a non-negative int")
        # why mana can be 0?
        if not isinstance(spell_power, int) or spell_power <= 0:
            raise ValueError("spell_power must be a positive int")

        self.attack_power = attack
        self.health = health
        self.mana = mana
        self.spell_power = spell_power

    # ---- Card contract ----
    def play(self, game_state: dict) -> dict:
        return {
            "card_played": self.name,
            "mana_used": self.cost,
            "effect": "Elite card enters the battlefield"
        }

    # Combines combat prowess with magical capabilities

    # ---- Combatable ----
    def attack(self, target) -> dict:
        target_name = getattr(target, "name", None) or str(target)
        return {
            "attacker": self.name,
            "target": target_name,
            "damage": self.attack_power,
            "combat_type": CombatType.MELEE.value,
        }

    def defend(self, incoming_damage: int) -> dict:
        if not isinstance(incoming_damage, int) or incoming_damage < 0:
            raise ValueError("incoming_damage must be a non-negative int")

        blocked = min(3, incoming_damage)
        taken = incoming_damage - blocked
        self.health -= taken
        return {
            "defender": self.name,
            "damage_taken": taken,
            "damage_blocked": blocked,
            "still _alive": self.health > 0,
        }

    def get_combat_stats(self) -> dict:
        return {"attack": self.attack_power, "health": self.health}

    # ---- Magical ----
    def cast_spell(self, spell_name: str, targets: list) -> dict:
        if not isinstance(spell_name, str) or not spell_name.strip():
            raise ValueError("spell_name must be a non-empty string")
        if not isinstance(targets, list):
            raise TypeError("targets must be a list")

        mana_used = min(4, self.mana)
        self.mana -= mana_used

        target_names = [getattr(t, "name", str(t)) for t in targets]
        return {
            "caster": self.name,
            "spell": spell_name.strip(),
            "targets": target_names,
            "mana_used": mana_used,
        }

    def channel_mana(self, amount: int) -> dict:
        if not isinstance(amount, int) or amount < 0:
            raise ValueError("amount must be a non-negative int")
        self.mana += amount
        return {"channeled": amount, "total_mana": self.mana}

    def get_magic_stats(self) -> dict:
        return {"mana": self.mana, "spell_power": self.spell_power}

# 1.
# 近战（melee）
# 魔法（magic）
# 2.
# ---- Card contract ----
# = 一个注释
# = 表示下面是 Card 类的“接口规范”
# = 通常和抽象类一起使用
# 3.
# min(3, incoming_damage) 是 Python 内置函数 min()，返回两个参数中较小的那个。
# 4. for demo purpose
# spell_power is not defined
# and  man can still cast spell even mana < 4
# 4.
# ABC vs Protocol
# class Combatable(ABC):
#     @abstractmethod
#     def attack(self, target):
#         pass
# 必须显式继承
# 不继承就不算 Combatable
# 是“名义类型系统”（Nominal Typing）
# 你必须声明“我是 Combatable”。
#
# Protocol（结构类型）
# from typing import Protocol
# class Combatable(Protocol):
#     def attack(self, target) -> dict:
#         ...
# 不需要继承
# 只要你有 attack() 方法
# 就自动被认为是 Combatable
# 是“结构类型系统”（Structural Typing）
# 只要你“长得像”，就算。
# 5.
# Diamond inheritance 的问题是：
# 同一个父类可能被调用两次。
# Python 用 MRO + super() 解决：
# 计算唯一调用顺序
# 每个类只执行一次
