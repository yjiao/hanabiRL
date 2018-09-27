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
        self.state = []
        self.feature_idx = {}

        for i in range(card.MIN_CARD_VALUE, card.MAX_CARD_VALUE + 1):
            for color in card.Color:
                if color == card.Color.UNK:
                    continue
                self.deck.add_card(card.Card(color=color, value=i))

        self._update_state()

    def _update_state(self):
        """Returns a list of the current state.
        hints
        bombs
        board
        deck
        discard
        players
        """
        state = []
        self.feature_idx['hints'] = len(state)
        state.append(self.hints)

        self.feature_idx['bombs'] = len(state)
        state.append(self.bombs)

        self.feature_idx['bombs'] = len(state)
        state.extend(self.board.to_list())

        self.feature_idx['deck'] = len(state)
        state.extend(self.deck.to_list())

        self.feature_idx['discard'] = len(state)
        state.extend(self.discard.to_list())

        self.feature_idx['players'] = []
        for player in self.players:
            self.feature_idx['players'].append(len(state))
            state.extend(player.to_list())

        self.state = state
        return state

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
