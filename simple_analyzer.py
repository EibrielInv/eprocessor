class SimpleAnalyzer:
    def __init__(self, script):
        self.script = script

    def analize(self, message):
        result = {
            "intents": [],
            "entities": [],
            "emotions": []
        }
        return result
