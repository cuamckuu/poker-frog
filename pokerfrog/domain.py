"""Module to implement domain classes."""

import dataclasses

CARD_VALUES = [
    '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A',
]
CARD_SUITS = ['spades', 'diamonds', 'hearts', 'clubs']


@dataclasses.dataclass
class Card:
    """Class to repesent card object."""

    value: str
    suit: str

    def __repr__(self):
        suit = {
            'spades': '♠',
            'diamonds': '♦',
            'hearts': '♥',
            'clubs': '♣',
        }[self.suit]

        return f'[{self.value} {suit}]'
