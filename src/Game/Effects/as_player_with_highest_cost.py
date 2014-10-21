from Game.Effects.effect_runner import PerformEffects

class AsPlayerWithHighestCost:
    """ Represents an effect to run as the Player who has the greatest cost of cards """
    
    def __init__(self, sourceType, thenEffects):
        """ Initialize the Effect with the children effects and the source to check from """
        self.sourceType = sourceType
        self.thenEffects = thenEffects
        
    def perform(self, context):
        """ Perform the Game Effect """
        players = self.findHighestCostPlayers(context)
        
        for player in players:
            newContext = context.getPlayerContext(player)
            
            coroutine = PerformEffects(self.thenEffects, newContext)
            response = yield coroutine.next()
            while True:
                response = yield coroutine.send(response)
                
    def findHighestCostPlayers(self, context):
        """ Return the players with the highest cost """
        players = []
        highCost = None
        for player in context.foes:
            cost = sum([card.cost for card in context.getPlayerContext(player).loadSource(self.sourceType)])
            if highCost is None or cost > highCost:
                players = [player]
                highCost = cost
            elif highCost == cost:
                players.append(player)
        
        return players