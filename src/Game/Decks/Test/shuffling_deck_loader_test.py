import unittest

from Game.Decks.shuffling_deck_loader import ShufflingDeckLoader
from kao_deck.deck_initializer import DeckInitializer

class loadDeck(unittest.TestCase):
    """ Test cases of loadDeck """
    
    def  setUp(self):
        """ Build the Deck Loader for the test """
        self.items = [1,2,3,4,5]
        deckInitializer = DeckInitializer()
        [deckInitializer.addItem(item, 1) for item in self.items]
        
        self.deckLoader = ShufflingDeckLoader(deckInitializer)
        
    def deckCreated(self):
        """ Test that the Deck was created and shuffled """
        deck = self.deckLoader.loadDeck()
        self.assertTrue(all([item in deck for item in self.items]), "Each item in the deck initializer should be in the deck")

# Collect all test cases in this class
testcasesLoadDeck = ["deckCreated"]
suiteLoadDeck = unittest.TestSuite(map(loadDeck, testcasesLoadDeck))

##########################################################

# Collect all test cases in this file
suites = [suiteLoadDeck]
suite = unittest.TestSuite(suites)

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(suite)