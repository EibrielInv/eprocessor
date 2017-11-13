class SimpleAnalyzer:
    def __init__(self, script):
        self.script = script

    def analize(self, message):
        result = {
            "intents": [],
            "entities": [],
            "emotions": []
        }
        if message is None:
            return result
        intents = self.script.get_intents()
        matching_intents = []
        for intent in intents:
            for example in intents[intent]["default"]["es"]:
                if message.lower() == example["text"].lower():
                    matching_intent = {
                        "confidence": 1.0,
                        "intent": intent
                    }
                    matching_intents.append(matching_intent)
        result["intents"] = matching_intents
        return result
