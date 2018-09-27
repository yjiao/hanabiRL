import unittest
import card


class TestCards(unittest.TestCase):
    def test_conversions(self):
        for color in card.Color:
            for val in range(card.MIN_CARD_VALUE, card.MAX_CARD_VALUE):
                card_ = card.int_to_card((card.card_to_int(card.Card(color, val))))
                self.assertEqual(card_.color, color)
                self.assertEqual(card_.value, val)

    def test_pile_operations(self):
        pile = card.Pile(card.PileType.DECK)
        color = card.Color.BLUE
        value = 5
        card_ = card.Card(color=color, value=value)

        pile.add_card(card_)
        self.assertIn(card_, pile.cards)
        pile.remove_card(card_)
        self.assertNotIn(card_, pile.cards)


if __name__ == "__main__":
    unittest.main()
