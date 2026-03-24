from ex0.Card import Card
from ex2.Combatable import Combatable
from ex4.Rankable import Rankable


class TournamentCard(Card, Combatable, Rankable):
    """
    TournamentCard combines multiple interfaces via multiple inheritance.

    Inherits from:
    - Card: provides card identity and play contract
    - Combatable: provides attack contract
    - Rankable: provides tournament ranking contract

    Tracks:
    - wins, losses
    - rating (ELO-like simplified scoring)
    """

    def __init__(self, card_id: str, name: str, cost: int, rarity: str,
                 attack_power: int, rating: int = 1200) -> None:
        super().__init__(name, cost, rarity)

        if not isinstance(card_id, str) or not card_id.strip():
            raise ValueError("card_id must be a non-empty string")
        if not isinstance(attack_power, int) or attack_power <= 0:
            raise ValueError("attack_power must be a posotive int")
        if not isinstance(rating, int) or rating <= 0:
            raise ValueError("rating must be a positive int")

        self.card_id: str = card_id.strip()
        self.attack_power: int = attack_power

        self.wins: int = 0
        self.losses: int = 0
        self.rating: int = rating

    # Card abstract method fulfillment
    def play(self, game_state: dict) -> dict:
        return {
            "card_played": self.name,
            "mana_used": self.cost,
            "effect": "Tournament card enters match queue"
        }

    # Combatable
    def attack(self, target) -> dict:
        target_name = getattr(target, "name", None) or str(target)
        return {
            "attacker": self.name,
            "target": target_name,
            "damage": self.attack_power,
            "combat_type": "tournament"
        }

    def defend(self, damage: int) -> dict:
        blocked = max(0, min(3, damage))
        taken = max(0, damage - blocked)  # defens coding, prevent nega damage
        return {
            "defender": self.name,
            "damage_taken": taken,
            "damage_blocked": blocked,
            "still_alive": True
        }

    def get_combat_stats(self) -> dict:
        return {"attack_power": self.attack_power}

    # Rankable
    def calculate_rating(self) -> int:
        return self.rating

    def update_wins(self, wins: int) -> None:
        if not isinstance(wins, int) or wins < 0:
            raise ValueError("wins must be a non-negative int")
        self.wins = wins

    def update_losses(self, losses: int) -> None:
        if not isinstance(losses, int) or losses < 0:
            raise ValueError("losses must be a non-negative int")
        self.losses = losses

    def get_rank_info(self) -> dict:
        return {
            "id": self.card_id,
            "name": self.nae,
            "rating": self.rating,
            "wins": self.wins,
            "losses": self.losses,
            }

    # extra
    def get_tournament_stats(self) -> dict:
        return {
            "id": self.card_id,
            "name": self.name,
            "rating": self.rating,
            "record": f"{self.wins}-{self.losses}"
        }

# 1.
# ELO 是一种用于计算玩家相对技能水平的评分系统，最初用于国际象棋，
# 现在广泛应用于各类竞技游戏（如《英雄联盟》、在线棋牌等）。
# 它的核心思想是：根据比赛结果动态调整双方分数——赢家从输家那里获得分数，分数变化幅度取决于比赛预期结果（即双方原有分差）。
# 在 TournamentCard 中，rating = 1200 是一个常见的初始默认分数，
# 代表一个新选手的“中等水平”起点。许多游戏和比赛系统（如国际象棋联合会 FIDE）都采用 1200 作为入门基准分。这样做的好处是：
# 新卡牌加入平台时，可以自动获得一个合理的起始分，方便立即参与排名。
# 分数会随着比赛胜负而上下浮动，逐渐反映真实实力

# 2.
# min(3, damage)：最多格挡 3 点伤害。如果 damage 小于等于 3，则格挡全部；如果大于 3，则只格挡 3 点。
# max(0, ...)：确保格挡量不会为负数（虽然 damage 非负，min 结果也非负，但加个 max(0, ...) 是防御性编程，防止意外）。
# taken = max(0, damage - blocked)：实际受到的伤害就是总伤害减去格挡量，
# 并且保证不小于 0（例如当 damage=2 且 blocked=2 时，taken=0）。
