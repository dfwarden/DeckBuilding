from source import Source

class EventSource(Source):
    """ Represents a potential source """
    
    def __init__(self, event):
        """ Initialize the source """
        sourceType = None
        if hasattr(event, "fromSource"):
            sourceType = event.fromSource.sourceType
        Source.__init__(self, event, sourceType=sourceType)