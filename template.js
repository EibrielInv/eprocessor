function (context, input_data, text) {
    goto = null;
    evaluate = false;
    text_title = "default";

    best_intent = null;
    best_intent_confidence = null;
    if (input_data["intents"].length > 0) {
        if (input_data["intents"][0]["confidence"] > 0.7) {
            best_intent = input_data["intents"][0]["intent"]
            best_intent_confidence = input_data["intents"][0]["confidence"];
        }
    }
    /*code*/
    returning = {
        "context": context,
        "text": text[text_title],
        "goto": goto,
        "evaluate": evaluate
    }
    return returning;
}
