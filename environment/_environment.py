from . import card


class Environment(object):
    def __init__(self, num_players):
        self.reset(num_players)

    def reset(self, num_players):
        self.players = [card.Pile(card.PileType.PLAYER)] * num_players
        self.num_players = num_players
        self.discard = card.Pile(card.PileType.DISCARD)
        self.deck = card.Pile(card.PileType.DECK)
        self.board = card.Pile(card.PileType.BOARD)
        self.hints = card.MAX_HINTS
        self.bombs = 0

        for i in range(card.MIN_CARD_VALUE, card.MAX_CARD_VALUE + 1):
            for color in card.Color:
                if color == card.Color.UNK:
                    continue
                self.deck.add_card(card.Card(color=color, value=i))

    def __repr__(self):
        return f"""
==============================================
Environment
----------------------------------------------
hints remaining: {self.hints}
bombs: {self.bombs}
num_players: {self.num_players}
players: {self.players}
discard: {self.discard}
deck: {self.deck}
board: {self.board}
==============================================
        """
