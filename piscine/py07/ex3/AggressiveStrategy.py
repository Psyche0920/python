from ex3.GameStrategy import GameStrategy


class AggressiveStrategy(GameStrategy):
    """
    Aggresive strategy:
    - Plays low-cost cards first
    - Prioritizes attacking the enemy player directly
    """

    TURN_MANA = 5

    def get_strategy_name(self) -> str:
        return "AggressiveStrategy"

    def prioritize_targets(self, available_targets: list) -> list:
        return sorted(available_targets,
                      key=lambda x: 0 if str(x) == "Enemy Player" else 1)

    def execute_turn(self, hand: list, battlefield: list) -> dict:
        remaining_mana = self.TURN_MANA
        hand_sorted = sorted(hand,
                             key=lambda c: getattr(c, "cost", 999))
        cards_played = []
        damage_dealt = 0
        targets_attacked = []

        for card in hand_sorted:
            if getattr(card, "cost", 999) <= remaining_mana:
                remaining_mana -= card.cost
                cards_played.append(card.name)

                info = card.get_card_info()
                ctype = info.get("type")

                if ctype == "Creature":
                    battlefield.append(card)
                    targets_attacked = self.prioritize_targets([
                        "Enemy Player"])
                    damage_dealt += getattr(card, "attack", 0)

                elif ctype == "Spell":
                    if card.name == "Lightning Bolt":
                        damage_dealt += 3
                        targets_attacked = self.prioritize_targets([
                            "Enemy Player"])
                else:
                    pass

        mana_used = self.TURN_MANA - remaining_mana

        return {
            "strategy": self.get_strategy_name(),
            "actions": {
                "cards_played": cards_played,
                "mana_used": mana_used,
                "targets_attacked": targets_attacked,
                "damage_dealt": damage_dealt,
            }
        }


# 手牌（hand）：在卡牌游戏中，指玩家手中尚未打出、可以使用的卡牌集合。
# hand 列表里每个元素都是 Card 类实例（或其子类，如 CreatureCard、SpellCard 等）。
# 作用：execute_turn 方法会根据策略（如 AggressiveStrategy）遍历 hand 中的卡牌，
# 判断哪些可以打出（费用足够），并记录打出的卡牌、造成的伤害等信息。
# battlefield（战场）则代表已经打出、在场上的卡牌列表（如生物卡）。
