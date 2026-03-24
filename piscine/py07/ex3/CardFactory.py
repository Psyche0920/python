from abc import ABC, abstractmethod
from ex0.Card import Card


class CardFactory(ABC):
    """Abstract Factory Interface"""

    @abstractmethod
    def create_creature(self, name_or_power: str | int | None = None) -> Card:
        raise NotImplementedError

    @abstractmethod
    def create_spell(self, name_or_power: str | int | None = None) -> Card:
        raise NotImplementedError

    @abstractmethod
    def create_artifact(self, name_or_power: str | int | None = None) -> Card:
        raise NotImplementedError

    @abstractmethod
    def create_themed_deck(self, size: int) -> dict:
        raise NotImplementedError

    @abstractmethod
    def get_supported_types(self) -> dict:
        raise NotImplementedError
