from abc import ABC, abstractmethod


class GameStrategy(ABC):
    """Abstract Strategy Interface"""

    @abstractmethod
    def execute_turn(self, hand: list, battlefield: list) -> dict:
        raise NotImplementedError

    @abstractmethod
    def get_strategy_name(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def prioritize_targets(self, available_targets: list) -> list:
        raise NotImplementedError
