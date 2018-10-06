import unittest
import card


class TestCards(unittest.TestCase):
    def test_conversions(self):
        for color in card.Color:
            for val in range(card.MIN_CARD_VALUE, card.MAX_CARD_VALUE):
                idx = card.get_card_index(card.Card(color, val))
                card_repr_actual = card.CARD_ARRAYS[idx]

                card_repr_expected = [0] * card.CARD_DIMENSION
                card_repr_expected[color] = 1
                card_repr_expected[len(card.Color) + val] = 1

                self.assertEqual(card_repr_actual, card_repr_expected)

    def test_pile_operations(self):
        pile = card.Pile(card.PileType.DECK)
        color = card.Color.BLUE
        value = 5
        card1 = card.Card(color=color, value=value)

        # add a card, now it's in the pile
        pile.add_card(card1)
        self.assertIn(card1, pile.cards)

        # add the same card, should have the same two cards in list
        # representation
        pile.add_card(card1)
        card_list_repr = pile.to_list()
        self.assertEqual(len(card_list_repr), 2)
        self.assertEqual(card_list_repr[0], card_list_repr[1])

        # remove a card, there's still another one in there
        pile.remove_card(card1)
        self.assertIn(card1, pile.cards)

        color = card.Color.RED
        value = 1
        card2 = card.Card(color=color, value=value)

        # add another card
        pile.add_card(card2)
        self.assertIn(card2, pile.cards)

        pile.remove_card(card1)
        self.assertNotIn(card1, pile.cards)
        pile.remove_card(card2)
        self.assertNotIn(card2, pile.cards)

        self.assertEqual(pile.to_list(), [])


if __name__ == "__main__":
    unittest.main()
