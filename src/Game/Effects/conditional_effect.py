from Game.Effects.effect_runner import PerformEffect

class ConditionalEffect:
    """ Represents an effect that conditionally applies """
    
    def __init__(self, condition, effect, otherwiseEffect=None):
        """ Initialize the Effect with the condition to evaluate and effect to perform """
        self.condition = condition
        self.effect = effect
        self.otherwiseEffect = otherwiseEffect
        
    def perform(self, args):
        """ Perform the Game Effect """
        coroutine = None
        if self.condition.evaluate(args):
            coroutine = self.performEffect(args)
        elif self.otherwiseEffect is not None:
            coroutine = self.performOtherwiseEffect(args)
            
        if coroutine is not None:
            response = yield coroutine.next()
            while True:
                response = yield coroutine.send(response)
                
    def performEffect(self, args):
        """ Perform the conditional effect """
        coroutine = PerformEffect(self.effect, args)
        response = yield coroutine.next()
        while True:
            response = yield coroutine.send(response)
            
    def performOtherwiseEffect(self, args):
        """ Perform the conditional effect """
        coroutine = PerformEffect(self.otherwiseEffect, args)
        response = yield coroutine.next()
        while True:
            response = yield coroutine.send(response)