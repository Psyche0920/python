from ex0.Card import Card


class ArtifactCard(Card):
    """
    ArtifactCard: permanent modifier card with durability & a described effect
    """

    def __init__(self, name: str, cost: int, rarity: str,
                 durability: int, effect: str):
        super().__init__(name, cost, rarity)

        if not isinstance(durability, int) or durability <= 0:
            raise ValueError("durability must be a positive int")
        if not isinstance(effect, str) or not effect.strip():
            raise ValueError("effect must be a non-empty string")

        self.durability: int = durability
        self.effect: str = effect.strip()

    def play(self, game_state: dict) -> dict:
        return {
            "card_played": self.name,
            "mana_used": self.cost,
            "effect": f"Permament: {self.effect}",
        }

    def activate_ability(self) -> dict:
        if self.durability <= 0:
            return {"artifact": self.name, "activated": False,
                    "reason": "Broken (0 durability)"}
        self.durability -= 1,
        return {
            "artifact": self.name,
            "activated": True,
            "remaining_durability": self.durability,
            "effect": self.effect,
        }

    def get_card_info(self) -> dict:
        info = super().get_card_info()
        info.update({"type": "Artifact", "durability": self.durability,
                     "effect": self.effect})
        return info
