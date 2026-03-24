from ex0.Card import Card


class CreatureCard(Card):
    """
    Concrete implementation of a creature-type card.

    A CreatureCard represents a <combat-capable card that can be summoned
    to the battlefield>. It extends the abstract Card base class by adding
    <combat-related attributes such as attack and health>.

    Attributes:
        attack (int): The offensive power of the creature (must be positive).
        health (int): The health points of the creature (must be positive).
    """
    def __init__(self, name: str, cost: int, rarity: str,
                 attack: int, health: int):
        """
        Initialize a CreatureCard instance.

        Args:
            name (str): Name of the creature.
            cost (int): Mana cost required to play the creature.
            rarity (str): Rarity classification of the card.
            attack (int): Attack value (must be a positive integer).
            health (int): Health value (must be a positive integer).

        Raises:
            ValueError: If attack or health are not positive integers.
        """
        super().__init__(name, cost, rarity)

        if not isinstance(attack, int) or attack <= 0:
            raise ValueError("attack must be a positive int")
        if not isinstance(health, int) or health <= 0:
            raise ValueError("health must be a positive int")

        self.attack = attack
        self.health = health

    def play(self, game_state: dict) -> dict:
        """
        Play the creature card.

        This method implements the abstract `play` contract defined
        in the Card base class. When played, the creature is considered
        summoned to the battlefield.

        Args:
            game_state (dict): The current state of the game.

        Returns:
            dict: A dictionary describing the result of playing the card.
        """
        return {
            "card_played": self.name,
            "mana_used": self.cost,
            "effect": "Creature summoned to battlefield",
            }

    def attack_target(self, target) -> dict:
        """
        Perform an attack against a target.

        Args:
            target: The target of the attack. Can be another card
                    or any object with a 'name' attribute.

        Returns:
            dict: A dictionary describing the combat outcome.
        """
        target_name = getattr(target, "name", None) or str(target)
        # get the value of name, if not get, None, then goes to or str(target)
        return {
            "attacker": self.name,
            "target": target_name,
            "damage_dealt": self.attack,
            "combat_resolved": True,
        }

    def get_card_info(self) -> dict:
        """
        Retrieve detailed information about the creature card.

        Extends the base Card information by adding creature-specific
        attributes such as attack and health.

        Returns:
            dict: A dictionary containing full card information.
        """
        info = super().get_card_info()
        info.update(
            {
                "type": "Creature",
                "attack": self.attack,
                "health": self.health
            }
        )
        return info
