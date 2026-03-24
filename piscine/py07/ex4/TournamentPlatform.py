from ex4.TournamentCard import TournamentCard


class TournamentPlatform:
    """
    TournamentPlatform manages tournament cards and matches.

    Responsibilities:
    - register cards and store them by ID
    - create matches and update wins/losses/ratings
    - provide leaderboard and platform report
    """

    RATING_DELTA = 16

    def __init__(self) -> None:
        self._cards: dict[str, TournamentCard] = {}
        self._matches_played: int = 0

    def register_card(self, card: TournamentCard) -> str:
        if not isinstance(card, TournamentCard):
            raise TypeError("card must be a TournamentCard")

        cid = card.card_id
        if cid in self._cards:
            raise ValueError(f"card_id already registered: {cid}")
        self._cards[cid] = card
        return cid

    def create_match(self, card1_id: str, card2_id: str) -> dict:
        if card1_id not in self._cards or card2_id not in self._cards:
            raise KeyError("both card IDs must be registered")
        if card1_id == card2_id:
            raise ValueError("Cannot match a card against itself")

        c1 = self._cards[card1_id]
        c2 = self._cards[card2_id]

        if c1.rating > c2.rating:
            winner, loser = c1, c2
        elif c2.rating > c1.rating:
            winner, loser = c2, c1
        else:
            if c1.attack_power >= c2.attack_power:
                winner, loser = (c1, c2)
            else:
                winner, loser = (c2, c1)

        winner.update_wins(winner.wins + 1)
        loser.update_losses(loser.losses + 1)

        winner.rating += self.RATING_DELTA
        loser.rating -= self.RATING_DELTA

        self._matches_played += 1
        return {
            "winner": winner.card_id,
            "loser": loser.card_id,
            "winner_rating": winner.rating,
            "loser_rating": loser.rating
        }

    def get_leaderboard(self) -> list:
        cards_sorted = sorted(self._cards.values(),
                              key=lambda c: c.rating, reverse=True)
        leaderboard = []
        for c in cards_sorted:
            leaderboard.append(
                {
                    "id": c.card_id,
                    "name": c.name,
                    "rating": c.rating,
                    "wins": c.wins,
                    "losses": c.losses
                }
            )
        return leaderboard

    def generate_tournament_report(self) -> dict:
        total_cards = len(self._cards)
        if total_cards == 0:
            avg_rating = 0
        else:
            avg_rating = round(sum(c.rating for c in
                                   self._cards.values()) / total_cards)
        return {
            "total_cards": total_cards,
            "matches_played": self._matches_played,
            "avg_rating": avg_rating,
            "platform_status": "active"
        }

# 1. KeyError 是什么？
# KeyError 是 Python 内置的异常，在尝试访问字典中不存在的键时抛出。
# 2. sorted(self._cards.values(), key=lambda c: c.rating) 是什么意思？
# self._cards.values() 返回字典中所有存储的 TournamentCard 对象组成的视图（可迭代）。
# sorted() 是 Python 内置函数，用于对可迭代对象排序，返回一个新的已排序列表，原对象不变。
# key=lambda c: c.rating 指定排序的依据：lambda c: c.rating 是一个匿名函数，
# 它接受一个参数 c（代表每个卡牌对象），返回该对象的 rating 属性值。sorted 会根据这个返回值的大小决定元素的顺序（默认升序）。
# 加上 reverse=True 后，按评级降序排列（从高到低）。
# 所以这行代码的作用是：将平台中所有已注册的卡牌按评级从高到低排序，得到一个列表，赋值给 cards_sorted。
