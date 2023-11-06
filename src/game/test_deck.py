import unittest
from deck import BirdDeck  # Assuming your Deck class is in a file named 'deck.py'
from bird_card import BirdCard  # Assuming your BirdCard class is in a file named 'bird_card.py'


class TestDeck(unittest.TestCase):

    def test_deck_initialization(self):
        deck = BirdDeck()
        self.assertIsInstance(deck.deck, list)
        self.assertIsInstance(deck.tray, list)
        self.assertEqual(len(deck.deck), 170)  # Adjust the number based on your deck size
        self.assertEqual(len(deck.tray), 3)

    def test_draw_from_deck(self):
        deck = BirdDeck()
        card = deck.draw_from_deck()
        self.assertIsInstance(card, BirdCard)

    def test_draw_from_tray(self):
        deck = BirdDeck()
        deck.draw_from_tray(0)
        self.assertEqual(len(deck.tray), 2)
        deck.draw_from_tray(1)
        self.assertEqual(len(deck.tray), 1)
        deck.draw_from_tray(0)
        self.assertEqual(len(deck.tray), 0)

    def test_refill_tray(self):
        deck = BirdDeck()
        deck.draw_from_tray(0)
        deck.draw_from_tray(0)
        self.assertEqual(len(deck.tray), 1)
        deck.refill_tray()
        self.assertEqual(len(deck.tray), 3)


if __name__ == '__main__':
    unittest.main()