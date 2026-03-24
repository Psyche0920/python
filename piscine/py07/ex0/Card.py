from abc import ABC, abstractmethod
from enum import Enum


class Rarity(Enum):
    """
    Enumeration representing valid rarity levels for cards.
    """
    COMMON = "Common"
    RARE = "Rare"
    LEGENDARY = "Legendary"


class Card(ABC):
    """
    Abstract base class representing a generic card in the DataDeck system.


    This class defines the common attributes and behaviors that all card types
    must implement. Concrete subclasses (e.g., CreatureCard, SpellCard, etc.)
    are required to implement the `play` method.

    Attributes:
        name (str): The name of the card.
        cost (int): The mana cost required to play the card.
        rarity (str): The rarity classification of the card.
    """

    def __init__(self, name: str, cost: int, rarity: str):
        """
        Initialize a Card with basic attributes.

        Args:
            name (str): The name of the card. Must be a non-empty string.
            cost (int): The mana cost. Must be a non-negative integer.
            rarity (str): The rarity level. Must be a non-empty string.

        Raises:
            ValueError: If any input validation fails.
        """
        if not isinstance(name, str) or not name.strip():
            raise ValueError("name must be a non-empty string")
        if not isinstance(cost, int) or cost < 0:
            raise ValueError("cost must be a non-negative int")
        if not isinstance(rarity, str) or not rarity.strip():
            # " "space means also empty, so it should not be "" or " "
            raise ValueError("rarity must be a non-empty string")

        self.name: str = name
        self.cost: int = cost
        self.rarity: Rarity = rarity

    @abstractmethod
    def play(self, game_state: dict) -> dict:
        """
        Execute the card's primary effect.

        This method must be implemented by all subclasses.
        It defines how the card interacts with the current game state.

        Args:
            game_state (dict): A dict representing the current game state.

        Returns:
            dict: A dictionary describing the result of playing the card.
        """
        raise NotImplementedError
        # dont use pass, it means impelement silently even error happens

    def get_card_info(self) -> dict:
        """
        Retrieve the card's basic information.

        Returns:
            dict: A dictionary containing the card's name, cost,
                  rarity, and inferred type.
        """
        return {
            "name": self.name,
            "cost": self.cost,
            "rarity": self.rarity,
            "type": self.__class__.__name__.replace("Card", "") or "Card",
            # Replace"Card" with "" if true(not empty) stop,
            # if False(empty)shw "Card"
            # if "Card" alone, will show "Card" not ""
        }

    def is_playable(self, available_mana: int) -> bool:
        """
        Determine whether the card can be played with the available mana.

        Args:
            available_mana (int): The current mana available to the player.

        Returns:
            bool: True if the player has enough mana to play the card,
                  otherwise False.
        """
        if not isinstance(available_mana, int) or available_mana < 0:
            return False
        return available_mana >= self.cost
