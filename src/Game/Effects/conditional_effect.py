from Game.Effects.effect_runner import PerformEffects, PerformEffect

class ConditionalEffect:
    """ Represents an effect that conditionally applies """
    
    def __init__(self, condition, effects, otherwiseEffect=None):
        """ Initialize the Effect with the condition to evaluate and effect to perform """
        self.condition = condition
        self.effects = effects
        self.otherwiseEffect = otherwiseEffect
        
    def perform(self, context):
        """ Perform the Game Effect """
        coroutine = None
        if self.condition.evaluate(context):
            coroutine = self.performEffects(context)
        elif self.otherwiseEffect is not None:
            coroutine = self.performOtherwiseEffect(context)
        else:
            context.failed = True
            
        if coroutine is not None:
            response = yield coroutine.next()
            while True:
                response = yield coroutine.send(response)
                
    def performEffects(self, context):
        """ Perform the conditional effect """
        coroutine = PerformEffects(self.effects, context)
        response = yield coroutine.next()
        while True:
            response = yield coroutine.send(response)
            
    def performOtherwiseEffect(self, context):
        """ Perform the conditional effect """
        coroutine = PerformEffect(self.otherwiseEffect, context)
        response = yield coroutine.next()
        while True:
            response = yield coroutine.send(response)