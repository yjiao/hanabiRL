import unittest
import card


class TestCards(unittest.TestCase):
    def test_conversions(self):
        for color in card.Color:
            for val in range(0, card.MAX_CARD_VALUE + 1):
                card_ = card.int_to_card((card.card_to_int(card.Card(color, val))))
                self.assertEqual(card_.color, color)
                self.assertEqual(card_.value, val)


if __name__ == "__main__":
    unittest.main()
