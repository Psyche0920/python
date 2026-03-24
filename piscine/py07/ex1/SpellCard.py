from ex0.Card import Card
from enum import Enum


class SpellEffect(Enum):
    """
    Enum representing all valid spell effect types.
    """
    DAMAGE = "damage"
    HEAL = "heal"
    BUFF = "buff"
    DEBUFF = "debuff"


class SpellCard(Card):
    """
    SpellCard: one-time instant effect card (damage/heal/buff/debuff).
    """

    # create a set Valid_EFFECTS for all valid effect types
    VALID_EFFECTS = {"damage", "heal", "buff", "debuff"}

    # check the validity of inputed effect_type:
    # non-empty str and in the valid effects set
    def __init__(self, name: str, cost: int, rarity: str, effect_type: str):
        super().__init__(name, cost, rarity)

        if not isinstance(effect_type, str) or not effect_type.strip():
            raise ValueError("effect_type must be a non-empty string")

        self.effect_type: SpellEffect = effect_type

# play and show the effect_type info
    def play(self, game_state: dict) -> dict:  # why two lines?
        effect_text = {
                "damage": "Deal 3 damage to target",
                "heal": "Heal 3 health to target",
                "buff": "Give +2 attack to target",
                "debuff": "Give -2 attack to target",
            }[self.effect_type]
        return {
            "card_played": self.name,
            "mana_used": self.cost,
            "effect": effect_text,
        }

    def resolve_effect(self, targets: list) -> dict:
        target_names = [getattr(t, "name", str(t)) for t in targets]
        return {
            "spell": self.name,
            "effect_type": self.effect_type,
            "targets": target_names,
            "resolved": True,
        }

    def get_card_info(self) -> dict:
        info = super().get_card_info()
        info.update({"type": "Spell", "effect_type": self.effect_type})
        return info


# 1. sorted(self.VALID_EFFECTS)
# 会把 set 排序成 list。
# set 是无序的
# sorted() 返回一个 排好序的列表
# 这样报错信息更整齐。
# 2. raise 会立即停止当前函数执行。
# 具体规则：
# 如果没有 try/except
# 程序会：
# 打印错误
# 终止当前程序
# 3. VALID_EFFECTS = {"damage", "heal", "buff", "debuff"}
# set, effective sorting, allow repetition
# 集合查找速度：
# set: O(1)
# list: O(n)
# 而且：
# set 表示“唯一值集合”
# list 表示“有顺序的序列”
# 这里明显是集合概念。
# 4.  effect_text = {
#           "damage": "Deal 3 damage to target",
#            "heal": "Heal 3 health to target",
#           "buff": "Give +2 attack to target",
#           "debuff": "Give -2 attack to target",
#       }[self.effect_type]
# effect_text is extracting the value of effect_type keys from a dict
# {...}[key] 创建字典，然后用 key 取值
# 5. def resolve_effect(self, targets: list) -> dict:
#     target_names = [getattr(t, "name", str(t)) for t in targets]
#     # list input, sequence, allow repetition
#     # if get the attribute of "name" in targets,
#     # use the value of "name", or simply str(t)
