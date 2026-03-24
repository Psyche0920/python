from abc import ABC, abstractmethod


class Rankable(ABC):
    """
    Rankable interface for tournament ranking.

    Any Rankable object must be able to:
    - calculate a rating score
    - track wins and losses
    - expose ranking info in a dict form
    """

    @abstractmethod
    def calculate_rating(self) -> int:
        """Return the current rating value. """
        raise NotImplementedError

    @abstractmethod
    def update_wins(self, wins: int) -> None:
        """Update win count. """
        raise NotImplementedError

    @abstractmethod
    def update_losses(self, losses: int) -> None:
        """Update loss count. """
        raise NotImplementedError

    @abstractmethod
    def get_rank_info(self) -> dict:
        """Return rank-related info such as rating and record. """
        raise NotImplementedError
