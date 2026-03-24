import random
from typing import List
from ex0.Card import Card


class Deck:
    """
    Deck: manages a collection of Card objects of any concrete subtype.
    """

    def __init__(self) -> None:
        self._cards: List[Card] = []

    def add_card(self, card: Card) -> None:
        if not isinstance(card, Card):
            raise TypeError("card must be an instance of Card")
        self._cards.append(card)

    def remove_card(self, card_name: str) -> bool:
        if not isinstance(card_name, str) or not card_name.strip():
            return False

        card_name = card_name.strip()
        for i, c in enumerate(self._cards):
            if c.name == card_name:
                del self._cards[i]
                return True
        return False

    def shuffle(self) -> None:
        random.shuffle(self._cards)

    def draw_card(self) -> Card:
        if not self._cards:
            raise IndexError("Cannot draw from an emtpy deck")
        return self._cards.pop(0)

    def get_deck_stats(self) -> dict:
        total = len(self._cards)
        if total == 0:
            return {"total_cards": 0, "creatures": 0, "spells": 0,
                    "avg_cost": 0.0}

        creatures = 0
        spells = 0
        artifacts = 0
        total_cost = 0

        for c in self._cards:
            info = c.get_card_info()
            ctype = info.get("type", "")
            if ctype == "Creature":
                creatures += 1
            elif ctype == "Spell":
                spells += 1
            elif ctype == "Artifact":
                artifacts += 1
            total_cost += c.cost

        return {
            "total_cards": total,
            "creatures": creatures,
            "spells": spells,
            "artifacts": artifacts,
            "avg_cost": round(total_cost / total, 2)  # keep two digits
        }

# 1. 在 remove_card 方法中，enumerate(self._cards) 的作用是在遍历列表的同时，同时获得每个元素的索引和元素本身。
# i 是当前元素在列表中的索引（从 0 开始）。
# c 是当前索引对应的元素，也就是一个 Card 对象（或其子类对象）。
# 好处：当找到名字匹配的卡牌时（c.name == card_name），可直接用 del self._cards[i] 通过索引 i 删除该元素
# 如不用 enumerate，需先找到元素对象再用 self._cards.remove(c) 删除，但 remove 方法也需遍历列表定位元素，效率相同。
# 不过使用索引删除可以明确告诉程序“删除这个位置上的元素”，代码意图更清晰。
# 此外，由于牌组中可能有多张同名卡牌，这段代码只删除第一个找到的，符合常见的“移除一张指定名称的卡牌”的需求。
# 2. random.shuffle(self._cards) 是 Python 标准库中 random 模块提供的函数，
# 用于就地随机打乱列表 self._cards 中元素的顺序。它不返回新列表，而是直接修改原列表。
# 3. IndexError 是 Python 内置的异常类型，表示序列下标超出范围。
# 在这里，当牌组为空时调用 draw_card()，代码会主动抛出 IndexError("Cannot draw from an empty deck")
# 提示调用者不能从空牌组中抽牌。这是一种防御性编程，避免后续操作出错
# 4. pop 是 Python 列表的一个方法，它的作用是移除列表中指定位置的元素，并返回被移除的元素。
# 如果不传参数，pop() 默认移除并返回列表的最后一个元素。
# 如果传入一个整数参数（如 pop(0)），它会移除并返回列表中该索引位置的元素。
# 5. consenting adults” philosophy
# 意思是：
# 程序员应该自律
# _ 是“请不要用”的信号
# 但如果你真的需要，你可以
# 6. def remove_card(self, card_name: str) -> bool:
#         if not isinstance(card_name, str) or not card_name.strip():
#             return False  # why not raise ValueError here?
# 如果“删除失败”是预期可能发生的情况 → return False
# 如果“传入参数本身就是错误” → raise
