"""Module to evaluate different game metrics."""

from pokerfrog.domain import GameState, CARD_VALUES


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


def get_hutchinson_score(hand_cards) -> int:
    """Return hand score, limp when over ~30, call or raise when over ~34."""
    if not all(hand_cards):
        return 0

    score = 0
    card1, card2 = hand_cards

    # Bonus for value
    values_bonus = {
        'A': 16,
        'K': 14,
        'Q': 13,
        'J': 12,
        '10': 11,
    }

    score += (values_bonus.get(card1.value) or int(card1.value))
    score += (values_bonus.get(card2.value) or int(card2.value))

    # Bonus for hand potential
    if card1.value == card2.value:
        score += 10

    if card1.suit == card2.suit:
        score += 4

    pos1, pos2 = CARD_VALUES.index(card1.value), CARD_VALUES.index(card2.value)

    # Shortest distance in circular list
    distance = abs(pos2 - pos1)
    distance = min(distance, len(CARD_VALUES) - distance)

    distance_bonus = {
        1: 3,
        2: 2,
        3: 1,
    }
    score += distance_bonus.get(distance, 0)

    # Bonus for position
    # TODO: Get dealer and blinds to do so
    # TODO: +3 points for mid-pos
    # TODO: +5 points for cut-off or button

    return score

