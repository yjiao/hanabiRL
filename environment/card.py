from collections import namedtuple
from enum import IntEnum
from random import shuffle

MAX_CARD_VALUE = 5
MIN_CARD_VALUE = 0
MAX_HINTS = 8
MAX_BOMBS = 3


Card = namedtuple("Card", ["color", "value"])


def card_to_int(card):
    return card.color * (MAX_CARD_VALUE) + card.value


def int_to_card(int_):
    color = int_ // (MAX_CARD_VALUE)
    value = int_ % (MAX_CARD_VALUE)
    return Card(color=color, value=value)


class Color(IntEnum):
    BLUE = 0
    GREEN = 1
    RED = 2
    WHITE = 3
    YELLOW = 4


class PileType(IntEnum):
    DISCARD = 1
    DECK = 2
    PLAYER = 3
    BOARD = 4


class Pile(object):
    def __init__(self, pile_type):
        self.type = pile_type
        self.cards = []

    def __repr__(self):
        rep = f"pile of type {self.type.name} ({self.type}) with {len(self.cards)} cards\n"
        for card in sorted(self.cards):
            rep += f"    card: {card.color.name: >8}, {card.value: >3} --> {card_to_int(card)}\n"
        return rep

    def to_list(self):
        max_deck_size = (MAX_CARD_VALUE) * (len(Color))
        output = [0] * max_deck_size
        for card in self.cards:
            output[card_to_int(card)] = 1
        return output

    def shuffle(self):
        shuffle(self.cards)

    def add_card(self, card):
        self.cards.append(card)

    def draw(self):
        assert self.type == PileType.DECK, f"Can only draw from DECK, current PileType is {self.type}"
        return self.cards.pop()

    def remove_card(self, card):
        for i, card_in_pile in enumerate(self.cards):
            if card_in_pile == card:
                self.cards.pop(i)
