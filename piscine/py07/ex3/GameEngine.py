from ex3.CardFactory import CardFactory
from ex3.GameStrategy import GameStrategy


class GameEngine:
    """
    Central coordinator of the card game simulation.

    The GameEngine connects the Abstract Factory (card creation)
    with the Strategy (decision-making logic) to simulate gameplay.

    Responsibilities:
        - Configure the engine with a card factory and strategy.
        - Maintain the player's hand and battlefield state.
        - Execute game turns using the selected strategy.
        - Track statistics such as turns simulated and total damage dealt.
    """

    def __init__(self) -> None:
        """
        Initialize the game engine with empty state.

        Attributes:
            factory (CardFactory | None):
                The card factory responsible for creating themed cards.

            strategy (GameStrategy | None):
                The strategy object that determines how a turn is played.

            hand (list):
                The list of cards currently available to the player.

            battlefield (list):
                Cards that have been played and are currently in play.

            turns_simulated (int):
                Counter tracking how many turns have been executed.

            total_damage (int):
                Accumulated damage dealt during the simulation.

            cards_created (int):
                Number of cards generated when the engine was configured.
        """

        self.factory: CardFactory | None = None
        self.strategy: GameStrategy | None = None  # ???
        self.hand: list = []
        self.battlefield: list = []

        self.turns_simulated = 0
        self.total_damage = 0
        self.cards_created = 0

    def configure_engine(self, factory: CardFactory,
                         strategy: GameStrategy) -> None:
        """
        Configure the game engine with a factory and a strategy.

        This method prepares the engine for gameplay by:
            - Assigning the card factory.
            - Assigning the gameplay strategy.
            - Generating an initial themed deck.
            - Populating the player's hand and battlefield.

        Args:
            factory (CardFactory):
                The factory used to create cards and themed decks.

            strategy (GameStrategy):
                The strategy that determines how turns are executed.
        """

        self.factory = factory
        self.strategy = strategy

        deck = factory.create_themed_deck(size=3)
        self.hand = deck.get("hand", [])
        self.battlefield = deck.get("battlefield", [])

        self.cards_created = len(self.hand)

    def simulate_turn(self) -> dict:
        """
        Execute a single game turn using the configured strategy.

        The strategy decides how cards in the hand are played and
        how targets are attacked. The engine records the resulting
        statistics such as damage dealt and number of turns simulated.

        Returns:
            dict:
                A dictionary describing the result of the executed turn,
                including strategy name and action summary.

        Raises:
            RuntimeError:
                If the engine has not been configured with a factory
                and strategy before running the simulation.
        """

        if self.factory is None or self.strategy is None:
            raise RuntimeError("Engine not configured")

        result = self.strategy.execute_turn(self.hand, self.battlefield)
        self.turns_simulated += 1
        self.total_damage += result["actions"]["damage_dealt"]
        return result

    def get_engine_status(self) -> dict:
        """
        Return a summary of the current simulation status.

        The status includes gameplay statistics collected during
        the simulation process.

        Returns:
            dict:
                A dictionary containing:
                    - turns_simulated: total number of turns executed
                    - strategy_used: name of the active strategy
                    - total_damage: cumulative damage dealt
                    - cards_created: number of cards initially generated

        Raises:
            RuntimeError:
                If the engine has not been configured yet.
        """

        if self.strategy is None:
            raise RuntimeError("Engine is not configured")

        return {
            "turns_simulated": self.turns_simulated,
            "strategy_used": self.strategy.get_strategy_name(),
            "total_damage": self.total_damage,
            "cards_created": self.cards_created
        }


# 1.
# deck.get("hand", []) 是 Python 字典的 get 方法，它尝试从字典中获取键 "hand" 对应的值：
# 如果键存在，则返回该值（即手牌列表）。
# 如果键不存在（例如字典结构意外改变），则返回默认值 []（空列表），避免程序因 KeyError 崩溃
# 2.
# RuntimeError 是 Python 内置的一个异常类，通常在程序运行时遇到无法继续执行的错误时抛出。
# 引擎在未配置（即未调用 configure_engine 注入工厂和策略）之前，不能执行回合模拟或获取状态。
# 如果开发者忘记先配置就调用这些方法，引擎会主动抛出 RuntimeError，
# 并附带清晰的错误信息 "Engine not configured"，提醒调用者必须先完成配置。
# 3.
# self.factory: CardFactory | None = None
# 含义：
# self.factory 变量
# 类型可以是 CardFactory 或 None
# 初始化时先设为 None
# 4. dict.get(key, default)
