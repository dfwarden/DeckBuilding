
class Turn:
    """ Represents a turn in the game """
    
    def __init__(self, player):
        """ Initialize the Turn """
        self.player = player
        self.power = 0
        self.playedCards = []
        
    def playCard(self, card):
        """ Play the provided card """
        self.player.hand.remove(card)
        card.play(self)
        self.playedCards.append(card)
        
    def gainPower(self, power):
        """ Gain the appropriate amount of power """
        self.power += power
        
    def __repr__(self):
        """ Return the String Representation of the Turn """
        return "<Turn: Power:{0}|Played:{1}>".format(self.power, self.playedCards)