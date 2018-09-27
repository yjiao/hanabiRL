from collections import namedtuple
from enum import IntEnum

MAX_CARD_VALUE = 5
MIN_CARD_VALUE = 1
MAX_HINTS = 8
MAX_BOMBS = 3


Card = namedtuple("Card", ["color", "value"])


class Color(IntEnum):
    UNK = 0
    BLUE = 1
    GREEN = 2
    RED = 3
    WHITE = 4
    YELLOW = 5


class PileType(IntEnum):
    DISCARD = 1
    DECK = 2
    PLAYER = 3
    BOARD = 4


class Pile(object):
    def __init__(self, pile_type):
        self.type = pile_type
        self.cards = set()

    def __repr__(self):
        rep = f"pile of type {self.type.name} ({self.type}) with {len(self.cards)} cards\n"
        for card in sorted(self.cards):
            rep += f"    card: {card.color.name: >8}, {card.value: >3}\n"
        return rep

    def add_card(self, card):
        self.cards.add(card)

    def remove_card(self, card):
        if card in self.cards:
            self.cards.remove(card)
        else:
            raise Exception(f"Card {card} is not in deck {self.type}.name.")
