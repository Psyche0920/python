from abc import ABC, abstractmethod


class Combatable(ABC):
    """
    Abstract interface for combat abilities.
    """

    @abstractmethod
    def attack(self, target) -> dict:
        """Attack a target and return combat result."""
        raise NotImplementedError

    @abstractmethod
    def defend(self, incoming_damage: int) -> dict:
        """Defend against incoming damage and return defense result."""
        raise NotImplementedError

    @abstractmethod
    def get_combat_stats(self) -> dict:
        """Return combat-related stats (e.g., attack, health)."""
        raise NotImplementedError
