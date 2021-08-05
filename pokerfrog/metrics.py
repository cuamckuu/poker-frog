"""Module to evaluate different game metrics."""

from pokerfrog.domain import GameState


def get_game_state(table_cards) -> GameState:
    """Return game state based on table length."""
    placed_cards = [c for c in table_cards if c]

    return {
        0: GameState.PREFLOP,
        1: GameState.FLOP,
        2: GameState.FLOP,
        3: GameState.FLOP,
        4: GameState.TURN,
        5: GameState.RIVER,
    }.setdefault(len(placed_cards), GameState.UNKNOWN)

