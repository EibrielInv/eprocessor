class SimpleAnalyzer:
    def __init__(self, script):
        self.script = script

    def analize(self, message):
        result = {
            "interactions": [],
            "entities": [],
            "emotions": []
        }
        if message is None:
            return result
        interactions = self.script.get_interactions()
        matching_interactions = []
        for interaction in interactions:
            example = interactions[interaction]["examples"][0]
            if message.lower() == example["lang_id:es"]["text"][0].lower():
                matching_interaction = {
                    "confidence": 1.0,
                    "interaction": interaction
                }
                matching_interactions.append(matching_interaction)
        result["interactions"] = matching_interactions
        return result
