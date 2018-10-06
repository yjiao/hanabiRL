from . import card
from . import action

CARDS_PER_PLAYER = 4


class Environment(object):
    def __init__(self, num_players):
        assert num_players > 0, "Number of players must be greater than 0."
        self.num_players = num_players
        self.reset()

    def reset(self):
        """Reset environment to start of a game."""
        self.next_player = 0
        self.cards_per_player = CARDS_PER_PLAYER
        self.players = [
            card.Pile(card.PileType.PLAYER) for i in range(self.num_players)
        ]
        self.known_colors = [
            [0] * self.cards_per_player for i in range(self.num_players)
        ]
        self.known_values = [
            [0] * self.cards_per_player for i in range(self.num_players)
        ]
        self.discard = card.Pile(card.PileType.DISCARD)
        self.deck = card.Pile(card.PileType.DECK)
        self.board = card.Pile(card.PileType.BOARD)
        self.hints = card.MAX_HINTS
        self.bombs = 0
        self.state = []
        self.feature_idx = {}  # this keeps track of where each feature is

        self._populate_deck()
        self.deck.shuffle()

        # deal cards to players
        for player in self.players:
            for c in range(self.cards_per_player):
                player.add_card(self.deck.draw())

        self._update_state()

    def _populate_deck(self):
        """Fully populate the deck."""
        for color in card.Color:
            for value in range(card.MIN_CARD_VALUE, card.MAX_CARD_VALUE):
                if value == card.MIN_CARD_VALUE:
                    for _ in range(3):
                        self.deck.add_card(card.Card(color=color, value=value))
                else:
                    for _ in range(2):
                        self.deck.add_card(card.Card(color=color, value=value))

        # deal cards to players
        self.deck.shuffle()
        for player in self.players:
            for c in range(self.cards_per_player):
                player.add_card(self.deck.draw())

        self._update_state()

    def draw_from_deck(self, player):
        if not self.deck.empty():
            top_card = self.deck.draw()

            self.players[player].add_card(top_card)
            self.known_colors[player].append(0)
            self.known_values[player].append(0)

            return top_card
        return None

    def remove_from_hand(self, player, index):
        removed_card = self.players[player].remove_card(index)

        self.known_colors[player].pop(index)
        self.known_values[player].pop(index)

        return removed_card

    def next_playable_value(self, color):
        value = 0

        for c in self.board:
            if c.color == color:
                value += 1

        return value

    def increment_hints(self):
        self.hints = min(self.hints + 1, card.MAX_HINTS)

    def step(self, action):
        p = self.next_player

        p_pile = self.players[player]
        p_known_colors = self.known_colors[player]
        p_known_values = self.known_values[player]

        if action.action_type == ActionType.HINT:
            pass
        elif action.action_type == ActionType.PLAY:
            played_card = self.remove_from_hand(p, action.index)

            if played_card.value == self.next_playable_value(played_card.color):
                self.board.add_card(played_card)
                if played_card.value == card.MAX_CARD_VALUE:
                    self.increment_hints()
                self.draw_from_deck(p)
            else:
                self.discard.add_card(played_card)
                self.bombs += 1
                self.draw_from_deck(p)
        elif action.action_type == ActionType.DISCARD:
            self.discard.add_card(self.remove_from_hand(p, action.index))
            self.increment_hints()
            self.draw_from_deck(p)

        self.next_player = (self.next_player + 1) % self.num_players

    def _update_state(self):
        """Returns a list of the current state.
        next_player
        hints
        bombs
        board
        discard
        players
        known_values
        known_colors
        """
        state = []
        self.feature_idx["next_player"] = len(state)
        state.append(self.next_player)

        self.feature_idx["hints"] = len(state)
        state.append(self.hints)

        self.feature_idx["bombs"] = len(state)
        state.append(self.bombs)

        self.feature_idx["board"] = len(state)
        state.extend(self.board.to_list())

        self.feature_idx["discard"] = len(state)
        state.extend(self.discard.to_list())

        self.feature_idx["players"] = []
        for player in self.players:
            self.feature_idx["players"].append(len(state))
            state.extend(player.to_list())

        self.feature_idx["known_values"] = []
        for kv in self.known_values:
            self.feature_idx["known_values"].append(len(state))
            state.extend(kv)

        self.feature_idx["known_colors"] = []
        for kc in self.known_colors:
            self.feature_idx["known_colors"].append(len(state))
            state.extend(kc)

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
