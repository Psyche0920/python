from abc import ABC, abstractmethod


class Magical(ABC):
    """
    Abstract interface for magic abilities.
    """


@abstractmethod
def cast_spell(self, spell_name: str, targets: list) -> dict:
    """Cast a spell on targets and return spell result."""
    raise NotImplementedError


@abstractmethod
def channel_spell(self, amount: int) -> dict:
    """Channel mana (increase available mana) and return result."""
    raise NotImplementedError


@abstractmethod
def get_magic_stats(self) -> dict:
    """Return magic-related stats (e.g., mana, spell_power)."""
    raise NotImplementedError

# cast_spell：消耗法力施法，并将目标列表转换为字符串列表。
# channel_mana：增加法力值。
