from Game.Effects.effect_runner import PerformEffects
from Game.Effects.move_card import MoveCard
from Game.Events.cards_event import CardsEvent
from Game.Events.gained_card_event import GainedCardEvent
from Game.Notifications.cards_notification import CardsNotification
from Game.Notifications.notification_types import GAINED_CARD
from Game.Zones.zone_types import DISCARD_PILE

class GainCard(MoveCard):
    """ Represents an effect to Gain a card """
    
    def __init__(self, fromZoneType, toZoneType=DISCARD_PILE, notificationType=GAINED_CARD):
        """ Initialize the Effect with the card to remove from play before discarding """
        self.notificationType = notificationType
        MoveCard.__init__(self, fromZoneType, toZoneType)
        
    def perform(self, context):
        """ Perform the Game Effect """
        MoveCard.perform(self, context)
        
        fromZone = context.loadZone(self.fromZoneType)
        toZone = context.loadZone(self.toZoneType)
        
        for card in fromZone:
            coroutine = self.callOnGainEffects(card, toZone, context)
            try:
                response = yield coroutine.next()
                while True:
                    response = yield coroutine.send(response)
            except StopIteration:
                pass
            coroutine = self.sendGainedEvent(card, context)
            try:
                response = yield coroutine.next()
                while True:
                    response = yield coroutine.send(response)
            except StopIteration:
                pass
            context.owner.gainedCards.append(card)
        context.addNotification(CardsNotification(self.notificationType, context.player, list(fromZone), private=self.isPrivate(fromZone, toZone)))
        
    def callOnGainEffects(self, card, toZone, context):
        """ Call the cards gained effects and send the gained event """
        context = context.copy()
        context.parent = card
        event = CardsEvent([card], toZone, context)
        coroutine = PerformEffects(card.onGainEffects, event.context)
        response = yield coroutine.next()
        while True:
            response = yield coroutine.send(response)
        
    def sendGainedEvent(self, card, context):
        """ Call the cards gained effects and send the gained event """
        context = context.copy()
        context.parent = card
        coroutine = context.sendEvent(GainedCardEvent(card, context))
        response = yield coroutine.next()
        while True:
            response = yield coroutine.send(response)
            
    def isPrivate(self, fromZone, toZone):
        """ Return if the gained card event is private """
        return not (fromZone.public or toZone.public)