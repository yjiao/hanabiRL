from collections import namedtuple
from enum import IntEnum

MAX_CARD_VALUE = 5
MIN_CARD_VALUE = 1
UNK_CARD_VALUE = 0
MAX_HINTS = 8
MAX_BOMBS = 3


Card = namedtuple("Card", ["color", "value"])


def card_to_int(card):
    return card.color * (MAX_CARD_VALUE + 1) + card.value


def int_to_card(int_):
    color = int_ // (MAX_CARD_VALUE + 1)
    value = int_ % (MAX_CARD_VALUE + 1)
    return Card(color=color, value=value)


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
            rep += f"    card: {card.color.name: >8}, {card.value: >3} --> {card_to_int(card)}\n"
        return rep

    def to_list(self):
        max_deck_size = (MAX_CARD_VALUE + 1) * (len(Color))
        output = [0] * max_deck_size
        for card in self.cards:
            output[card_to_int(card)] = 1
        return output

    def add_card(self, card):
        self.cards.add(card)

    def remove_card(self, card):
        if card in self.cards:
            self.cards.remove(card)
        else:
            raise Exception(f"Card {card} is not in deck {self.type}.name.")
