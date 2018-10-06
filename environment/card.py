from collections import namedtuple
from enum import IntEnum
from random import shuffle

MAX_CARD_VALUE = 5
MIN_CARD_VALUE = 0
MAX_HINTS = 8
MAX_BOMBS = 3


Card = namedtuple("Card", ["color", "value"])


def get_card_index(card):
    return card.color * (MAX_CARD_VALUE) + card.value


class Color(IntEnum):
    BLUE = 0
    GREEN = 1
    RED = 2
    WHITE = 3
    YELLOW = 4


# initialize card array values
# [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
# [----color----] [----value---]
CARD_DIMENSION = MAX_CARD_VALUE + len(Color)
CARD_ARRAYS = [[0] * CARD_DIMENSION for _ in range(MAX_CARD_VALUE * len(Color))]
for color in Color:
    for val in range(MIN_CARD_VALUE, MAX_CARD_VALUE):
        CARD_ARRAYS[color * MAX_CARD_VALUE + val][color] = 1
        CARD_ARRAYS[color * MAX_CARD_VALUE + val][len(Color) + val] = 1


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
            rep += f"    card: {card.color.name: >8}, {card.value: >3} --> {CARD_ARRAYS[get_card_index(card)]}\n"
        return rep

    def to_list(self):
        output = [[0] * CARD_DIMENSION for _ in range(len(self.cards))]
        for i, card in enumerate(self.cards):
            output[i] = CARD_ARRAYS[get_card_index(card)]
        return output

    def shuffle(self):
        shuffle(self.cards)

    def add_card(self, card):
        self.cards.append(card)

    def draw(self):
        assert (
            self.type == PileType.DECK
        ), f"Can only draw from DECK, current PileType is {self.type}"
        return self.cards.pop()

    def remove_card(self, card):
        for i, card_in_pile in enumerate(self.cards):
            if card_in_pile == card:
                self.cards.pop(i)
